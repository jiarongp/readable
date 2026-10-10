Gradient accumulation lets you train with a batch that is too large to fit in memory at once. You run the forward and backward pass on several small slices of the batch, add their gradients together, and take one optimizer step at the end. Done correctly, that step is mathematically the same as a step on the whole batch. The exceptions, covered at the end, come from layers and losses that look at other examples in the batch.

## Purpose

The memory a training step needs grows with the batch size, because backpropagation stores the activations of every example in the batch. If the batch size you want does not fit on your hardware, you have two options. You can train with a smaller batch, which changes the optimization dynamics and may force you to retune the learning rate. Or you can keep the intended batch size and compute it in pieces. Gradient accumulation is the second option.

It trades time for memory, not compute for memory. The pieces run one after another, so the total work is the same as for the whole batch, and the wall time is usually a little longer because each kernel has less data to parallelize over.

## Mechanism

The standard training loop is: zero the gradients, run forward and backward, step the optimizer. Accumulation changes one thing: you run forward and backward several times before stepping. This works because `backward()` in frameworks such as PyTorch does not overwrite the stored gradient; it adds to it. Four backward passes without a `zero_grad()` in between leave the sum of four gradients in `.grad`.

The parameters stay fixed during all four passes, because the optimizer has not stepped yet. That is what makes adding the gradients legitimate: all four are gradients of the same loss terms at the same point in parameter space, so their sum is the gradient of their sum.

Schematically, with a batch split into four microbatches:

```python
optimizer.zero_grad()
for microbatch in split(batch, 4):
    loss = loss_fn(model(microbatch)) / 4   # mean loss on this microbatch, scaled
    loss.backward()                         # adds this microbatch's gradient to .grad
clip_grad_norm_(model.parameters(), max_norm)   # if you clip, clip the accumulated gradient
optimizer.step()
```

Anything that acts on the gradient, such as clipping, belongs after the loop and before the step, so it sees the full gradient rather than a quarter of it. The learning-rate scheduler, if any, also advances once per optimizer step, not once per microbatch.

## Why the loss is divided by 4

Suppose the full batch has $N = 4m$ examples and the training loss is the mean of per-example losses $\ell_i$. The gradient you want is

$$
\nabla L = \frac{1}{N}\sum_{i=1}^{N}\nabla \ell_i .
$$

Each microbatch $k$ holds $m$ examples, and its own mean loss is $L_k = \frac{1}{m}\sum_{i \in k}\ell_i$. If you call `backward()` on $L_k$ unscaled four times, the accumulated gradient is $\sum_k \nabla L_k = \frac{1}{m}\sum_i \nabla\ell_i$, which is $4\,\nabla L$. The sum of four means is four times the overall mean. Dividing each microbatch loss by 4 before `backward()` fixes this: $\sum_k \frac{1}{4}\nabla L_k = \frac{1}{4m}\sum_i \nabla\ell_i = \nabla L$, exactly.

A hypothetical one-parameter case makes the arithmetic visible. Say the four microbatch mean gradients are 2.0, −1.0, 3.0, and 0.0. The full-batch gradient is their mean, 1.0. Accumulating them unscaled gives 4.0. Scaling each by 1/4 gives 0.5 − 0.25 + 0.75 + 0.0 = 1.0, which matches.

Two notes on this rule:

- Dividing the loss by 4 before `backward()` and dividing `.grad` by 4 after the loop are equivalent, because the gradient is linear in the loss. The loss-side version is more common because it needs no extra pass over the parameters.
- The factor 1/4 is correct only because the microbatches are the same size. With unequal sizes $n_k$, weight microbatch $k$ by $n_k / N$ instead. The same applies when the loss is averaged over tokens rather than examples: four microbatches of equal sequence count can carry different token counts, and then the weights should be token counts, not 1/4.

If you forget the scaling, plain SGD behaves as if the learning rate were four times larger, since $\theta - \eta \cdot 4g = \theta - (4\eta) g$. Adam's update is close to invariant to a constant rescaling of the gradient, so the mistake is easy to miss there, but it still shifts anything that reads the raw gradient, such as clipping thresholds and logged gradient norms.

## When the result differs from one big batch

The identity above assumes each example's loss depends only on that example and the parameters. Whenever examples in the batch interact, splitting the batch changes the computation itself, not just its arrangement.

**Batch normalization.** BatchNorm computes the mean and variance of each activation over the current batch. With microbatches of size $m$, those statistics come from $m$ examples instead of $4m$, so every forward pass differs from the full-batch one, and the gradients differ with it. The running statistics used at inference are also updated four times per step instead of once. LayerNorm, RMSNorm, and GroupNorm normalize within a single example, so they are unaffected.

**Losses that pair examples.** A contrastive loss with in-batch negatives gives each example $m - 1$ negatives instead of $4m - 1$. The microbatched objective is a different, easier objective, and no scaling factor recovers the full-batch gradient. Any loss with a batch-level term, such as a normalization over the whole batch's predictions, has the same problem.

**Numerical differences.** Even for a pure per-example loss, the two procedures add the same terms in a different order, so the results agree only to floating-point rounding. This is negligible when gradients are stored in 32-bit floats, which is the usual case under mixed-precision autocast. If gradients themselves are kept in 16-bit, accumulating four small contributions can lose precision. Note the name clash here: "loss scaling" in fp16 training means multiplying the loss by a large constant to prevent gradient underflow, which is a separate mechanism from the 1/4 factor above, and the two multiply together.

**Randomness.** Dropout masks and data augmentations are drawn per forward pass, so the microbatched run uses different random draws than the full-batch run would. This is ordinary sampling noise, not a systematic difference; neither version is more correct.

In short: for a model without batch-dependent layers and a loss that is a mean over examples, four scaled microbatches give the same gradient as the combined batch, up to rounding. For models with BatchNorm or batch-coupled losses, accumulation gives you the memory savings but not the equivalence, and the effective batch size for those components stays at $m$.
