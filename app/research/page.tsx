import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = { title: "Technical Whitepaper", description: "The architecture, assumptions, validation plan, and open research questions behind Pocket Pet AI." };

export default function ResearchPage() {
  return (
    <main style={{ minHeight: "100vh", background: "#07101f", color: "white" }}>
      <nav className="nav shell" style={{ borderColor: "#293342" }}>
        <Link className="brand" href="/"><span className="brand-mark">p</span><span>Pocket Pet AI</span></Link>
        <Link className="nav-cta" href="/">Back to system <span>↗</span></Link>
      </nav>
      <section className="shell" style={{ padding: "76px 0 36px" }}>
        <p className="section-kicker light">Technical whitepaper · v0.1</p>
        <h1 style={{ fontSize: "clamp(48px,7vw,92px)", marginBottom: 28 }}>From frozen weights<br />to physical dataflow.</h1>
        <p style={{ color: "#9eabba", maxWidth: 720, fontSize: 17, lineHeight: 1.7 }}>A falsifiable architecture proposal covering ternary computation, mixed-precision escape paths, latent KV memory, streaming speech, safe tool control, FPGA mapping, and the measurements required before custom silicon.</p>
        <div className="hero-actions"><a className="button button-primary" href="/research/pocket-pet-ai-whitepaper.pdf" download>Download PDF <span>↓</span></a></div>
      </section>
      <section className="shell" style={{ paddingBottom: 80 }}>
        <div style={{ overflow: "hidden", borderRadius: 20, border: "1px solid #303b4c", background: "white", minHeight: "76vh" }}>
          <iframe title="Pocket Pet AI technical whitepaper" src="/research/pocket-pet-ai-whitepaper.pdf" style={{ width: "100%", height: "76vh", border: 0 }} />
        </div>
      </section>
    </main>
  );
}
