// Read-it word display: split a whitespace token into leading punctuation, the word core, trailing punctuation.
// Leading marks (opening quotes, brackets) stay on the left, trailing marks stay on the right.
// `wordUnits` capitalises only the first LETTER of the first grapheme ("wh" -> "Wh", never "WH").
// Pure, no DOM, so tools/scan_read_text.mjs can reuse it.
export function splitToken(tok) {
  const m = /^([^A-Za-z]*)(.*?)([^A-Za-z]*)$/s.exec(tok);
  return { lead: m[1], core: m[2], trail: m[3], bare: m[2].replace(/[^A-Za-z']/g, '') };
}

export function wordUnits(bare, e) {
  if (!e) return [bare];
  if (/^[A-Z]{2,}$/.test(bare)) return e.g.map(g => g.toUpperCase()); // acronym in the source ("IT"): keep it all capitals
  const cap = /^[A-Z]/.test(bare);
  return e.g.map((g, i) => (i === 0 && cap ? g.charAt(0).toUpperCase() + g.slice(1) : g));
}
