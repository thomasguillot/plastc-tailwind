const rgb = (hex: string) => [1, 3, 5].map((i) => parseInt(hex.substr(i, 2), 16) / 255);

export function wcag(a: string, b: string) {
  const lum = (hex: string) => {
    const [r, g, bl] = rgb(hex).map((v) => (v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4)));
    return 0.2126 * r + 0.7152 * g + 0.0722 * bl;
  };
  const x = lum(a);
  const y = lum(b);
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
}

export function apca(text: string, bg: string) {
  const Y = (hex: string) => {
    const [r, g, b] = rgb(hex).map((v) => Math.pow(v, 2.4));
    const y = 0.2126729 * r + 0.7151522 * g + 0.072175 * b;
    return y > 0.022 ? y : y + Math.pow(0.022 - y, 1.414);
  };
  const t = Y(text);
  const b = Y(bg);
  if (Math.abs(b - t) < 0.0005) return 0;
  if (b > t) {
    const s = (Math.pow(b, 0.56) - Math.pow(t, 0.57)) * 1.14;
    return s < 0.1 ? 0 : (s - 0.027) * 100;
  }
  const s = (Math.pow(b, 0.65) - Math.pow(t, 0.62)) * 1.14;
  return s > -0.1 ? 0 : (s + 0.027) * 100;
}
