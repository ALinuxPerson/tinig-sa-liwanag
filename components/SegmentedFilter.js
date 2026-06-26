import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { animate, motion, useMotionValue, useTransform } from "framer-motion";

const SPRING = { type: "spring", stiffness: 380, damping: 34 };
const PAD = 4;
const MAG = 1.16;

export default function SegmentedFilter({ options, value, onChange }) {
  const trackRef = useRef(null);
  const [trackW, setTrackW] = useState(0);
  const n = options.length;
  const activeIdx = Math.max(0, options.findIndex((o) => o.id === value));
  const slotW = trackW > 0 ? (trackW - 2 * PAD) / n : 0;

  const pillX = useMotionValue(0);
  const dragging = useRef(false);

  // clone shifts left as pill moves right — keeps active label centered under pill
  const cloneX = useTransform(pillX, (v) => -v);

  useLayoutEffect(() => {
    const el = trackRef.current;
    if (!el) return;
    const measure = () => setTrackW(el.offsetWidth);
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  useEffect(() => {
    if (dragging.current || slotW === 0) return;
    const ctrl = animate(pillX, activeIdx * slotW, SPRING);
    return () => ctrl.stop();
  }, [activeIdx, slotW, pillX]);

  function handleDragEnd() {
    dragging.current = false;
    const nearest = Math.round(
      Math.min(Math.max(pillX.get(), 0), (n - 1) * slotW) / slotW
    );
    animate(pillX, nearest * slotW, SPRING);
    if (options[nearest].id !== value) onChange(options[nearest].id);
  }

  return (
    <div
      ref={trackRef}
      role="tablist"
      style={{
        position: "relative",
        display: "inline-flex",
        borderRadius: 999,
        padding: PAD,
        background: "rgba(0,0,0,0.07)",
        boxShadow:
          "inset 0 2px 5px rgba(0,0,0,0.13), inset 0 -1px 0 rgba(255,255,255,0.6)",
        flexWrap: "nowrap",
      }}
    >
      {/* base label row — sets track width, always rendered */}
      {options.map((opt) => (
        <button
          key={opt.id}
          role="tab"
          aria-selected={value === opt.id}
          onClick={() => onChange(opt.id)}
          style={{
            flex: 1,
            border: "none",
            background: "transparent",
            borderRadius: 999,
            padding: "5px 14px",
            fontSize: "0.78rem",
            fontWeight: 500,
            color: "rgba(0,0,0,0.4)",
            cursor: "pointer",
            whiteSpace: "nowrap",
            position: "relative",
            zIndex: 10,
            userSelect: "none",
          }}
        >
          {opt.label}
        </button>
      ))}

      {/* draggable liquid-glass pill */}
      {slotW > 0 && (
        <motion.div
          style={{
            position: "absolute",
            top: PAD,
            bottom: PAD,
            left: PAD,
            width: slotW,
            x: pillX,
            zIndex: 20,
            borderRadius: 999,
            // clip-path beats overflow:hidden for clipping transformed children
            clipPath: "inset(0 round 999px)",
            cursor: "grab",
          }}
          drag="x"
          dragConstraints={{ left: 0, right: (n - 1) * slotW }}
          dragElastic={0.05}
          dragMomentum={false}
          onDragStart={() => { dragging.current = true; }}
          onDragEnd={handleDragEnd}
          whileTap={{ cursor: "grabbing" }}
        >
          {/* glass surface */}
          <div
            aria-hidden
            style={{
              position: "absolute",
              inset: 0,
              borderRadius: 999,
              background:
                "linear-gradient(to bottom, rgba(255,255,255,0.92), rgba(230,234,242,0.95))",
              backdropFilter: "blur(18px) saturate(200%) brightness(1.1)",
              WebkitBackdropFilter: "blur(18px) saturate(200%) brightness(1.1)",
              boxShadow:
                "inset 0 2.5px 2px rgba(255,255,255,1), inset 0 -2px 3px rgba(0,0,0,0.09), 0 1px 3px rgba(0,0,0,0.12)",
            }}
          />

          {/* magnified clone — cloneX counter-translates so active label stays centered;
              transformOrigin center keeps scale anchored to pill center */}
          <motion.div
            aria-hidden
            style={{
              pointerEvents: "none",
              position: "absolute",
              top: 0,
              bottom: 0,
              left: 0,
              width: n * slotW,
              display: "flex",
              alignItems: "center",
              x: cloneX,
              scale: MAG,
              transformOrigin: "center center",
              zIndex: 10,
            }}
          >
            {options.map((opt) => (
              <span
                key={opt.id}
                style={{
                  width: slotW,
                  flexShrink: 0,
                  textAlign: "center",
                  fontSize: "0.78rem",
                  fontWeight: 700,
                  color: "rgba(0,0,0,0.85)",
                  whiteSpace: "nowrap",
                  padding: "5px 0",
                }}
              >
                {opt.label}
              </span>
            ))}
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}
