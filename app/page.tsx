import Image from "next/image";
import Link from "next/link";
import {
  ArrowUpRight,
  Cpu,
  Database,
  Github,
  Lock,
  Microphone,
  NavArrowRight,
  OpenBook,
} from "iconoir-react";

const principles = [
  {
    icon: Cpu,
    title: "Co-designed compute",
    body: "A frozen model turns weight layout and execution order into hardware inputs.",
  },
  {
    icon: Database,
    title: "Stable memory core",
    body: "Latent working memory keeps active context compact while personal memory stays writable.",
  },
  {
    icon: Microphone,
    title: "Contextual sensing",
    body: "Audio-first perception wakes the larger system only when the moment needs it.",
  },
  {
    icon: Lock,
    title: "Private by architecture",
    body: "Inference, permissions, and long-term memory remain under the user’s control.",
  },
];

const papers = [
  {
    image: "/product-v1/research/paper-bitnet.png",
    label: "Ternary models",
    title: "The Era of 1-bit LLMs",
    detail: "BitNet b1.58 · primary paper",
  },
  {
    image: "/product-v1/research/paper-mla.png",
    label: "Latent attention",
    title: "DeepSeek-V2",
    detail: "Compressed attention · primary paper",
  },
  {
    image: "/product-v1/research/paper-finn.png",
    label: "FPGA acceleration",
    title: "FINN",
    detail: "Quantized networks on FPGA · primary paper",
  },
];

export default function Home() {
  return (
    <main className="product-page" id="top">
      <nav className="site-nav product-shell" aria-label="Primary navigation">
        <Link className="mobile-wordmark" href="#top" aria-label="Pocket Pet AI home">
          <Image src="/favicon.svg" alt="" width={24} height={24} />
          <span>Pocket Pet AI</span>
        </Link>
        <div className="site-links">
          <a href="#research">Research</a>
          <a href="#hardware">Hardware</a>
          <a href="https://github.com/sanjuhs/pocket-pet-ai">Open source</a>
          <a href="#roadmap">Roadmap</a>
        </div>
        <a className="nav-action" href="https://github.com/sanjuhs/pocket-pet-ai">
          Join the research preview <NavArrowRight width={16} height={16} />
        </a>
      </nav>

      <section className="living-hero product-shell">
        <div className="hero-intro">
          <h1>The Living Object.</h1>
          <p className="hero-subtitle">Private. Stable. Evolving with you.</p>
          <p className="hero-summary">
            A personal AI companion that lives on-device. It listens, remembers, and acts—without the cloud.
          </p>
        </div>
        <div className="hero-product">
          <Image
            src="/product-v1/hero/product-family.png"
            alt="Concept rendering of the Pocket Pet AI compute puck and two open-ear clips"
            fill
            priority
            sizes="(max-width: 900px) 100vw, 1280px"
          />
        </div>
        <p className="claim-note">Concept-stage research system. Not for sale.</p>
        <div className="hero-proof" aria-label="Product principles">
          <span><b>Runs locally</b>No cloud required</span>
          <span><b>Personal by design</b>Your data stays with you</span>
          <span><b>Tiny and efficient</b>All-day on small power</span>
          <span><b>Open and verifiable</b>Docs, code, and models</span>
        </div>
      </section>

      <section className="story-panel story-listens" id="hardware">
        <div className="story-visual">
          <Image src="/product-v1/story/listens-macro.png" alt="Macro concept rendering of the puck microphone apertures and soft-touch shell" fill loading="eager" sizes="100vw" />
        </div>
        <div className="story-copy product-shell">
          <h2>It listens.</h2>
          <p>Three low-power microphones capture the world around you. Open-ear audio keeps you present, not isolated.</p>
          <span className="figure-label">Figure · concept<br />Microphone response remains to be measured</span>
        </div>
      </section>

      <section className="story-panel story-remembers">
        <div className="story-visual">
          <Image src="/product-v1/story/exploded-memory.png" alt="Exploded concept rendering of the puck shell, compute boards, memory, thermal layer, and battery" fill sizes="100vw" />
        </div>
        <div className="story-copy product-shell">
          <h2>It remembers.</h2>
          <p>A stable memory architecture lets your companion build a lasting model of you—without sending a byte to the cloud.</p>
          <span className="figure-label">Figure · target<br />Final components and layout may differ</span>
        </div>
      </section>

      <section className="story-panel story-acts" id="acts">
        <div className="story-visual">
          <Image src="/product-v2/story/acts-light.png" alt="Concept macro rendering of a model-specific accelerator inside the compute puck" fill sizes="100vw" />
        </div>
        <div className="story-copy product-shell">
          <h2>It acts.</h2>
          <p>On-device reasoning proposes each action in milliseconds. A deterministic policy gate authorizes consequential execution.</p>
          <span className="figure-label">Figure · concept<br />No custom silicon has been fabricated</span>
        </div>
      </section>

      <section className="principles product-shell" id="principles">
        <header className="center-header">
          <h2>Built from first principles.</h2>
          <p>One fixed model. One inspectable system. Every assumption exposed to measurement.</p>
        </header>
        <div className="principle-grid">
          {principles.map(({ icon: Icon, title, body }) => (
            <article key={title}>
              <Icon width={30} height={30} strokeWidth={1.4} aria-hidden="true" />
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="reference-evidence" id="research">
        <div className="product-shell">
          <header className="center-header">
            <h2>Research and evidence.</h2>
            <p>Transparent methods. Measured results. Open to scrutiny.</p>
          </header>
          <div className="reference-evidence-grid">
            <article>
              <h3>Model ablations <span>(measured)</span></h3>
              <p>Outlier protection and latent memory are evaluated on checked-in software references.</p>
              <div className="evidence-mini evidence-mini-chart"><Image src="/product-v1/research/evidence.png" alt="Measured model-ablation charts" fill sizes="420px" /></div>
              <small>Figure · measured software reference</small>
            </article>
            <article>
              <h3>FPGA golden-vector pathway <span>(simulated)</span></h3>
              <p>Bit-accurate validation establishes a deterministic baseline before board measurements.</p>
              <div className="evidence-mini"><Image src="/product-v1/story/acts-silicon.png" alt="FPGA-oriented accelerator concept rendering" fill sizes="420px" /></div>
              <small>Figure · simulated, not board data</small>
            </article>
            <article className="paper-downloads">
              <h3>Primary papers &amp; downloads</h3>
              <p>Read our paper, methods, and the primary sources behind each hypothesis.</p>
              <a href="/research/pocket-pet-ai-whitepaper.pdf"><OpenBook width={19} height={19} />Pocket Pet AI technical whitepaper <span>PDF · 2.4 MB</span></a>
              <a href="https://github.com/sanjuhs/pocket-pet-ai/tree/main/research/papers"><OpenBook width={19} height={19} />Ternary-model research library <span>16 primary papers</span></a>
              <a href="https://github.com/sanjuhs/pocket-pet-ai/tree/main/benchmark-results"><OpenBook width={19} height={19} />Reproducible result artifacts <span>JSON · code · configs</span></a>
              <a className="download-all" href="https://github.com/sanjuhs/pocket-pet-ai/blob/main/docs/research-guide.md">View all papers and datasets <ArrowUpRight width={15} height={15} /></a>
            </article>
          </div>
        </div>
      </section>

      <section className="technical-theatre" id="roadmap">
        <div className="product-shell technical-intro">
          <p className="quiet-label quiet-label-blue">The architecture</p>
          <h2>Ternary weights.<br />Latent memory.<br />Real recall.</h2>
          <p>
            We re-imagine the model and memory system together—so your AI can adapt continually without forgetting.
          </p>
        </div>
        <div className="product-shell technical-grid">
          <article>
            <div className="technical-visual"><Image src="/product-v2/architecture/ternary-lattice.png" alt="Ternary-weight lattice visualization" fill sizes="360px" /></div>
            <h3>Ternary-native compute</h3>
            <p>Weights in −1, 0, and +1 reduce memory movement while preserving a protected high-precision path for outliers.</p>
            <strong>−1 / 0 / +1 <small>architecture</small></strong>
          </article>
          <article>
            <div className="technical-visual"><Image src="/product-v2/architecture/latent-memory.png" alt="Compact latent-memory block visualization" fill sizes="360px" /></div>
            <h3>Latent working memory</h3>
            <p>The software reference compresses K/V state into an int8 latent plus a per-token FP16 scale.</p>
            <strong>15.06× <small>measured payload ratio</small></strong>
          </article>
          <article>
            <div className="technical-visual technical-chart"><Image src="/product-v1/research/evidence.png" alt="Measured software trend lines" fill sizes="360px" /></div>
            <h3>Continual adaptation</h3>
            <p>Writable personal memory stays separate from frozen model weights, with retrieval tested independently.</p>
            <strong>Local <small>design requirement</small></strong>
          </article>
        </div>
      </section>

      <section className="evidence-section" id="evidence">
        <div className="product-shell evidence-head">
          <div>
            <p className="quiet-label">The evidence</p>
            <h2>Built to be proven.</h2>
          </div>
          <p>We test the architecture on real software references and bit-accurate simulations before making hardware claims.</p>
        </div>
        <div className="product-shell evidence-showcase">
          <article>
            <div className="showcase-image showcase-chart"><Image src="/product-v1/research/evidence.png" alt="Measured software-reference results" fill sizes="480px" /></div>
            <h3>Software benchmarks <span>(measured)</span></h3>
            <p>Outlier protection reduces injected-outlier error from 0.897 to 0.193; the latent cache reaches a 15.06× payload ratio.</p>
          </article>
          <article>
            <div className="showcase-image"><Image src="/product-v1/story/acts-silicon.png" alt="Accelerator concept used beside the simulated FPGA evidence" fill sizes="480px" /></div>
            <h3>FPGA pathway <span>(simulated)</span></h3>
            <p>The packed ternary golden vector matches explicit routed add/subtract exactly. This is not board performance.</p>
          </article>
        </div>
        <div className="product-shell evidence-actions">
          <a className="text-link" href="https://github.com/sanjuhs/pocket-pet-ai/tree/main/benchmark-results">
            Inspect the run artifacts <ArrowUpRight width={17} height={17} />
          </a>
          <a className="text-link" href="https://github.com/sanjuhs/pocket-pet-ai/tree/main/fpga">
            Review the FPGA golden model <ArrowUpRight width={17} height={17} />
          </a>
        </div>
      </section>

      <section className="open-research-section" id="open-research">
        <div className="product-shell research-heading">
          <div>
            <p className="quiet-label">The research</p>
            <h2>Open research.<br />Real rigor.</h2>
            <p>Deep dives, datasets, and design notes for researchers and builders.</p>
            <Link className="text-link" href="/research">Read the whitepaper <ArrowUpRight width={17} height={17} /></Link>
            <a className="text-link secondary-research-link" href="https://github.com/sanjuhs/pocket-pet-ai/blob/main/docs/research-guide.md">Browse technical docs <ArrowUpRight width={17} height={17} /></a>
          </div>
          <div className="research-books" aria-label="Open research documents">
            <div className="research-cover"><Image src="/product-v1/whitepaper/cover.png" alt="Pocket Pet AI whitepaper cover" fill sizes="300px" /></div>
            <div className="research-paper research-paper-one"><Image src={papers[0].image} alt="BitNet primary paper" fill sizes="360px" /></div>
            <div className="research-paper research-paper-two"><Image src={papers[1].image} alt="DeepSeek-V2 primary paper" fill sizes="360px" /></div>
          </div>
        </div>
      </section>

      <footer className="product-footer" id="footer">
        <div className="product-shell footer-claim">
          <h2>Concept today.<br />Foundation for tomorrow.</h2>
          <p>Pocket Pet AI is active research in local inference, memory, safety, and model-specific acceleration.</p>
          <a className="text-link text-link-light" href="https://github.com/sanjuhs/pocket-pet-ai">
            Join the open project <Github width={18} height={18} />
          </a>
        </div>
        <div className="product-shell footer-metrics">
          <span><b>7–9B</b>model class · target</span>
          <span><b>&lt;300 ms</b>response start · target</span>
          <span><b>8–15 W</b>conversation · estimate</span>
          <span><b>−1 / 0 / +1</b>ternary symbols · architecture</span>
        </div>
        <div className="product-shell footer-bottom">
          <div className="wordmark wordmark-light"><Image src="/favicon.svg" alt="" width={20} height={20} /><span>Pocket Pet AI</span></div>
          <nav aria-label="Footer navigation"><a href="#hardware">Hardware</a><a href="#evidence">Evidence</a><Link href="/research">Whitepaper</Link><a href="https://github.com/sanjuhs/pocket-pet-ai">GitHub</a></nav>
          <p>MIT licensed · concept stage</p>
        </div>
      </footer>
    </main>
  );
}
