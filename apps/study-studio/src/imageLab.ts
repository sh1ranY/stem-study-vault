/** Original grayscale stimuli. Every displayed plot and image uses these same samples. */
export const IMAGE_SIZE = 96;
export type LabControls = {
  passes: number;
  row: number;
  noise: number;
  pattern: "scene" | "stripes";
};
export const DEFAULT_CONTROLS: LabControls = {
  passes: 2,
  row: 48,
  noise: 0.12,
  pattern: "scene",
};
const clip = (v: number) => Math.min(1, Math.max(0, v));
export function makeImage(
  pattern: LabControls["pattern"],
  size = IMAGE_SIZE,
): Float64Array {
  const a = new Float64Array(size * size);
  for (let y = 0; y < size; y++)
    for (let x = 0; x < size; x++) {
      const u = x / size,
        v = y / size;
      let value = 0.18;
      if (pattern === "stripes") {
        // Four exact periods on the left, twelve on the right half, periodic over 48 pixels.
        const period = x < size / 2 ? size / 8 : size / 24;
        value = 0.5 + 0.35 * Math.cos((2 * Math.PI * x) / period);
      } else {
        if (u > 0.08 && u < 0.44 && v > 0.12 && v < 0.84) value = 0.82;
        if (u > 0.16 && u < 0.36 && v > 0.24 && v < 0.72) value = 0.18;
        if (u > 0.43 && u < 0.76 && v > 0.1 && v < 0.35)
          value = 0.5 + 0.35 * Math.cos((2 * Math.PI * x) / 12);
        if (u > 0.43 && u < 0.91 && v > 0.42 && v < 0.64)
          value = 0.5 + 0.35 * Math.cos((2 * Math.PI * x) / 4);
        if (u > 0.5 && u < 0.9 && v > 0.72 && v < 0.9 && u + v > 1.39)
          value = 0.82;
      }
      a[y * size + x] = value;
    }
  return a;
}
export function addNoise(image: Float64Array, amplitude: number): Float64Array {
  let seed = 1729;
  return Float64Array.from(image, (value) => {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return clip(value + amplitude * ((2 * seed) / 4294967296 - 1));
  });
}
export function smoothImage(
  image: Float64Array,
  passes: number,
  size = IMAGE_SIZE,
): Float64Array {
  let current = image.slice();
  const at = (x: number, y: number) =>
    ((y + size) % size) * size + ((x + size) % size);
  for (let p = 0; p < passes; p++) {
    const horizontal = new Float64Array(image.length),
      result = new Float64Array(image.length);
    for (let y = 0; y < size; y++)
      for (let x = 0; x < size; x++)
        horizontal[at(x, y)] =
          0.25 * current[at(x - 1, y)] +
          0.5 * current[at(x, y)] +
          0.25 * current[at(x + 1, y)];
    for (let y = 0; y < size; y++)
      for (let x = 0; x < size; x++)
        result[at(x, y)] =
          0.25 * horizontal[at(x, y - 1)] +
          0.5 * horizontal[at(x, y)] +
          0.25 * horizontal[at(x, y + 1)];
    current = result;
  }
  return current;
}
export function imageRow(
  image: Float64Array,
  row: number,
  size = IMAGE_SIZE,
): number[] {
  return Array.from(image.slice(row * size, (row + 1) * size));
}
export function response(frequency: number, passes = 1): number {
  return Math.pow(Math.cos(Math.PI * frequency), 2 * passes);
}
