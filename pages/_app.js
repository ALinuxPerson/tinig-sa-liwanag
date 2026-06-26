import localFont from "next/font/local";
import "../styles/globals.css";

const hangout = localFont({
  src: "../public/fonts/Benedict Regular.otf",
  variable: "--font-hangout",
  display: "swap",
});

export default function App({ Component, pageProps }) {
  return (
    <div className={hangout.variable}>
      <Component {...pageProps} />
    </div>
  );
}
