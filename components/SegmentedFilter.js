export default function SegmentedFilter({ options, value, onChange }) {
  return (
    <div
      role="tablist"
      style={{
        display: "inline-flex",
        flexWrap: "wrap",
        gap: 4,
        padding: 4,
        borderRadius: 999,
        background: "rgba(0,0,0,0.07)",
        boxShadow:
          "inset 0 2px 5px rgba(0,0,0,0.13), inset 0 -1px 0 rgba(255,255,255,0.6)",
      }}
    >
      {options.map((opt) => {
        const active = value === opt.id;
        return (
          <button
            key={opt.id}
            role="tab"
            aria-selected={active}
            onClick={() => onChange(opt.id)}
            style={{
              border: "none",
              borderRadius: 999,
              padding: "5px 14px",
              fontSize: "0.78rem",
              fontWeight: active ? 700 : 500,
              color: active ? "rgba(0,0,0,0.85)" : "rgba(0,0,0,0.4)",
              cursor: "pointer",
              whiteSpace: "nowrap",
              userSelect: "none",
              transition: "all 0.18s ease",
              background: active
                ? "linear-gradient(to bottom, rgba(255,255,255,0.92), rgba(230,234,242,0.95))"
                : "transparent",
              backdropFilter: active ? "blur(18px) saturate(200%)" : "none",
              WebkitBackdropFilter: active ? "blur(18px) saturate(200%)" : "none",
              boxShadow: active
                ? "inset 0 2px 2px rgba(255,255,255,1), inset 0 -2px 3px rgba(0,0,0,0.09), 0 1px 3px rgba(0,0,0,0.12)"
                : "none",
            }}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
