import Image from "next/image";
import Link from "next/link";

const targets = [
  ["7–9B", "frozen omni model"],
  ["~1.58-bit", "native ternary weights"],
  ["< 300 ms", "response-start ambition"],
  ["8–15 W", "conversation envelope"],
];

const layers = [
  { index: "01", title: "Listen", body: "An open-ear wearable keeps the acoustic front end light, local, and always ready." },
  { index: "02", title: "Reason", body: "A pocket compute puck runs one frozen, hardware-shaped multimodal model." },
  { index: "03", title: "Remember", body: "Encrypted episodic memory stays separate from the hot context and under your control." },
  { index: "04", title: "Act", body: "A deterministic permission layer brokers every tool call across phone and desktop." },
];

export default function Home() {
  return (
    <main>
      <nav className="nav shell" aria-label="Primary navigation">
        <Link className="brand" href="#top" aria-label="Pocket Pet AI home">
          <span className="brand-mark">p</span>
          <span>Pocket Pet AI</span>
        </Link>
        <div className="nav-links">
          <Link href="#system">System</Link>
          <Link href="#roadmap">Roadmap</Link>
          <Link href="/research">Research</Link>
        </div>
        <a className="nav-cta" href="https://github.com/sanjuhs/pocket-pet-ai" aria-label="View the open-source project on GitHub">
          Open source <span>↗</span>
        </a>
      </nav>

      <section className="hero shell" id="top">
        <div className="hero-copy">
          <div className="eyebrow"><span className="live-dot" /> Open architecture · concept stage</div>
          <h1>A personal AI<br />with a <em>pulse.</em></h1>
          <p className="hero-lede">
            One private model. One consistent personality. A voice in your ear and a frozen-model brain in your pocket—built to think, remember, and act without the cloud.
          </p>
          <div className="hero-actions">
            <Link className="button button-primary" href="/research">Read the whitepaper <span>↗</span></Link>
            <a className="button button-quiet" href="#system">Explore the system <span>↓</span></a>
          </div>
          <p className="microcopy">Research prototype, not a shipping hardware claim.</p>
        </div>
        <div className="hero-visual">
          <Image src="/images/pocket-pet-in-use.png" alt="Concept rendering of the Pocket Pet AI wearable, pocket puck, and phone companion" fill priority sizes="(max-width: 900px) 100vw, 56vw" />
          <div className="signal-card">
            <span className="wave">▂▅▇▃▆▂▅</span>
            <div><b>Voice loop active</b><small>local · encrypted · streaming</small></div>
          </div>
          <div className="latency-chip"><span>Target</span><b>&lt;300 ms</b><small>speech start</small></div>
        </div>
      </section>

      <section className="target-strip" aria-label="Design targets">
        <div className="shell target-grid">
          {targets.map(([value, label]) => <div className="target" key={label}><strong>{value}</strong><span>{label}</span></div>)}
          <div className="target-note">Design targets<br />to validate</div>
        </div>
      </section>

      <section className="manifesto shell section-pad">
        <p className="section-kicker">The premise</p>
        <h2>The model stops changing.<br /><span>The relationship doesn’t.</span></h2>
        <div className="manifesto-grid">
          <p className="big-copy">Freeze the neural architecture, co-design the silicon around its exact dataflow, and keep personal adaptation in encrypted memory—not in ever-changing weights.</p>
          <p className="body-copy">General-purpose accelerators pay a flexibility tax. Pocket Pet AI explores the opposite bet: one known low-bit model, fixed routing, protected precision where it matters, and software-defined tools around a stable personality core.</p>
        </div>
      </section>

      <section className="system-section" id="system">
        <div className="shell section-pad">
          <div className="section-head">
            <div><p className="section-kicker light">System architecture</p><h2>Voice. Brain. Hands.</h2></div>
            <p>Three physical surfaces, one continuous local experience.</p>
          </div>
          <div className="architecture-card">
            <Image src="/images/pocket-pet-architecture.png" alt="Exploded architecture concept for the Pocket Pet AI compute puck" fill sizes="(max-width: 900px) 100vw, 86vw" />
          </div>
          <div className="layer-grid">
            {layers.map((layer) => (
              <article className="layer" key={layer.index}>
                <span>{layer.index}</span><h3>{layer.title}</h3><p>{layer.body}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="frozen shell section-pad">
        <div className="frozen-copy">
          <p className="section-kicker">Frozen on purpose</p>
          <h2>Less movement.<br />More velocity.</h2>
          <p>In a ternary matrix, ordinary weights become add, subtract, or skip. Fix those weights before fabrication and the memory paths, sparsity map, and compute schedule become physical design inputs.</p>
          <div className="formula" aria-label="Ternary weight equation">
            <span>w<sub>i</sub> ∈</span><b>−1</b><b>0</b><b>+1</b><span>→</span><strong>ADD · SKIP · SUB</strong>
          </div>
        </div>
        <div className="memory-map">
          <div className="memory-top"><span>PROPOSED MEMORY MAP</span><span>9B-class model</span></div>
          <div className="memory-bar">
            <div className="segment ternary"><span>TERNARY CORE</span><b>~2.25 GB*</b></div>
            <div className="segment precision"><span>PROTECTED</span><b>mixed</b></div>
            <div className="segment runtime"><span>RUNTIME</span><b>8–16 GB</b></div>
          </div>
          <div className="memory-notes">
            <p><b>98%+</b><span>candidate low-bit pathway</span></p>
            <p><b>32–256 MB</b><span>on-chip scratch target</span></p>
            <p><b>64–256 MB</b><span>typical latent KV target</span></p>
          </div>
          <small>*Two-bit physical packing before scales, metadata, protected weights, and multimodal modules. Values are architecture targets, not measured silicon.</small>
        </div>
      </section>

      <section className="roadmap-section" id="roadmap">
        <div className="shell section-pad">
          <div className="section-head dark-head">
            <div><p className="section-kicker">Build sequence</p><h2>Software truth<br />before silicon.</h2></div>
            <p>Each stage exists to retire a different class of risk.</p>
          </div>
          <div className="stage-grid">
            <article className="stage featured">
              <div className="stage-number">STAGE 01 <span>NOW</span></div>
              <h3>Reference model<br />on commodity compute</h3>
              <p>Prove the complete speech-to-action loop, ternary emulation, latent-memory behavior, safety controller, and honest latency baseline.</p>
              <ul><li>Reproducible PyTorch prototype</li><li>Android + desktop tool bridge</li><li>Power, memory, TTFT benchmarks</li><li>Small-model accuracy harness</li></ul>
            </article>
            <article className="stage">
              <div className="stage-number">STAGE 02 <span>NEXT</span></div>
              <h3>Fixed-dataflow<br />FPGA demonstrator</h3>
              <p>Move the best-understood kernels into configurable logic and measure real bandwidth, utilization, thermals, and quality.</p>
              <ul><li>Ternary add/sub/skip arrays</li><li>Static weight-bank placement</li><li>Latent-KV memory controller</li><li>Streaming multi-token decoder</li></ul>
            </article>
          </div>
          <div className="gate-row"><span>Architecture gate</span><p>No ASIC recommendation until the FPGA system reproduces quality and demonstrates a defensible energy-per-token advantage.</p></div>
        </div>
      </section>

      <section className="safety shell section-pad">
        <div className="safety-visual"><Image src="/images/pocket-pet-product-system.png" alt="Pocket Pet AI product family and companion application concept" fill sizes="(max-width: 900px) 100vw, 48vw" /></div>
        <div className="safety-copy">
          <p className="section-kicker">Agency, with boundaries</p>
          <h2>The model proposes.<br />The controller decides.</h2>
          <p>The neural model never receives unrestricted control. Every action is typed, policy-checked, permission-scoped, observed, and—when sensitive—confirmed by the human.</p>
          <div className="action-flow"><span>Intent</span><i>→</i><span>Proposal</span><i>→</i><span>Policy</span><i>→</i><span>Consent</span><i>→</i><span>Action</span></div>
        </div>
      </section>

      <section className="research-cta">
        <div className="shell research-inner">
          <p className="section-kicker light">Open research</p>
          <h2>Read the architecture.<br />Challenge the assumptions.<br /><em>Help make it real.</em></h2>
          <p>The whitepaper exposes the math, tradeoffs, failure modes, staged validation plan, and open questions behind the product thesis.</p>
          <div className="hero-actions">
            <Link className="button button-white" href="/research">Open whitepaper <span>↗</span></Link>
            <a className="button button-outline" href="/research/pocket-pet-ai-whitepaper.pdf" download>Download PDF <span>↓</span></a>
          </div>
        </div>
      </section>

      <footer className="footer shell">
        <div className="brand"><span className="brand-mark">p</span><span>Pocket Pet AI</span></div>
        <p>Private intelligence, physically yours.</p>
        <div><Link href="/research">Whitepaper</Link><a href="https://github.com/sanjuhs/pocket-pet-ai">GitHub ↗</a><span>MIT licensed</span></div>
      </footer>
    </main>
  );
}
