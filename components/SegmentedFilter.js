export default function SegmentedFilter({ options, value, onChange }) {
  return (
    <div role="tablist" className="seg">
      {options.map((opt) => {
        const active = value === opt.id;
        return (
          <button
            key={opt.id}
            role="tab"
            aria-selected={active}
            onClick={() => onChange(opt.id)}
            className={`segBtn ${active ? "segActive" : ""}`}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
