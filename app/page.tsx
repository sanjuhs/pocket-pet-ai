import Image from "next/image";
import Link from "next/link";
import {
  ArrowUpRight,
  Brain,
  Cpu,
  Database,
  Download,
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
        <Link className="wordmark" href="#top" aria-label="Pocket Pet AI home">
          <Image src="/favicon.svg" alt="" width={24} height={24} />
          <span>Pocket Pet AI</span>
        </Link>
        <div className="site-links">
          <a href="#research">Research</a>
          <a href="#hardware">Hardware</a>
          <a href="https://github.com/sanjuhs/pocket-pet-ai">Open source</a>
          <a href="#evidence">Evidence</a>
        </div>
        <a className="nav-action" href="https://github.com/sanjuhs/pocket-pet-ai">
          Join the research preview <NavArrowRight width={16} height={16} />
        </a>
      </nav>

      <section className="living-hero product-shell">
        <div className="hero-intro">
          <p className="quiet-label">Open architecture · concept stage</p>
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
          <span><b>Built for one model</b>Hardware shaped around the weights</span>
          <span><b>Open and verifiable</b>Code, tests, and papers</span>
        </div>
      </section>

      <section className="story-panel story-listens" id="hardware">
        <div className="story-visual">
          <Image src="/product-v1/story/listens-macro.png" alt="Macro concept rendering of the puck microphone apertures and soft-touch shell" fill loading="eager" sizes="100vw" />
        </div>
        <div className="story-copy product-shell">
          <h2>It listens.</h2>
          <p>Low-power acoustic sensing stays ready. The larger model wakes only when context calls for it.</p>
          <span className="figure-label">Concept visualization · microphone response remains to be measured</span>
        </div>
      </section>

      <section className="story-panel story-remembers">
        <div className="story-visual">
          <Image src="/product-v1/story/exploded-memory.png" alt="Exploded concept rendering of the puck shell, compute boards, memory, thermal layer, and battery" fill sizes="100vw" />
        </div>
        <div className="story-copy product-shell">
          <h2>It remembers.</h2>
          <p>A compressed working context and encrypted personal memory build continuity without sending a life to the cloud.</p>
          <span className="figure-label">Concept visualization · final components and layout may differ</span>
        </div>
      </section>

      <section className="story-panel story-acts">
        <div className="story-visual">
          <Image src="/product-v1/story/acts-silicon.png" alt="Concept macro rendering of a model-specific accelerator inside the compute puck" fill sizes="100vw" />
        </div>
        <div className="story-copy product-shell light-copy">
          <h2>It acts.</h2>
          <p>The model proposes each action. Deterministic software checks permission, risk, and consent before execution.</p>
          <span className="figure-label">Concept visualization · no custom silicon has been fabricated</span>
        </div>
      </section>

      <section className="principles product-shell">
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

      <section className="technical-theatre" id="research">
        <div className="product-shell technical-intro">
          <p className="quiet-label quiet-label-blue">The architecture</p>
          <h2>Ternary weights.<br />Latent memory.<br />Real recall.</h2>
          <p>
            Freeze what should stay stable. Compress what must stay fast. Keep the user’s evolving memory separate, encrypted, and retrievable.
          </p>
        </div>
        <div className="product-shell technical-grid">
          <article>
            <Cpu width={28} height={28} strokeWidth={1.35} />
            <span>01 · Frozen compute</span>
            <h3>Add. Subtract. Skip.</h3>
            <p>Ordinary ternary weights route activations through three known operations. Protected outliers retain higher precision.</p>
            <strong>−1&nbsp;&nbsp;&nbsp;0&nbsp;&nbsp;&nbsp;+1</strong>
          </article>
          <article>
            <Database width={28} height={28} strokeWidth={1.35} />
            <span>02 · Latent working memory</span>
            <h3>More context. Fewer bytes.</h3>
            <p>The software reference compresses K/V state into an int8 latent plus a per-token FP16 scale.</p>
            <strong>15.06× <small>measured payload ratio</small></strong>
          </article>
          <article>
            <Brain width={28} height={28} strokeWidth={1.35} />
            <span>03 · Personal recall</span>
            <h3>History without surveillance.</h3>
            <p>Structured memories can be retrieved when relevant without keeping an entire life in the active context window.</p>
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
          <p>
            This is not a performance theatre. Every public number is tied to code, a run artifact, or an explicit target—and every failed premise is useful evidence.
          </p>
        </div>
        <div className="product-shell evidence-graphic">
          <Image src="/product-v1/research/evidence.png" alt="Measured software-reference results for outlier protection and latent cache compression" fill loading="eager" sizes="(max-width: 900px) 100vw, 1280px" />
        </div>
        <div className="product-shell evidence-ledger">
          <article><span>Measured · software</span><b>0.897 → 0.193</b><p>Injected-outlier relative-L2 error with 1% FP32 protection.</p></article>
          <article><span>Measured · software</span><b>15.06×</b><p>Tensor-payload reduction for the default 32-wide latent cache.</p></article>
          <article><span>Simulated · FPGA reference</span><b>Exact match</b><p>Packed ternary golden vector equals explicit routed add/subtract.</p></article>
          <article><span>Analytical · not board data</span><b>4.0×</b><p>Packed 2-bit weights versus dense int8 storage for the reference kernel.</p></article>
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

      <section className="open-research-section">
        <div className="product-shell research-heading">
          <div>
            <p className="quiet-label">The literature</p>
            <h2>Open research.<br />Real rigor.</h2>
          </div>
          <div>
            <p>Sixteen primary papers, verified locally and organized around the questions this architecture must answer.</p>
            <a className="text-link" href="https://github.com/sanjuhs/pocket-pet-ai/blob/main/docs/research-guide.md">
              Browse the research guide <ArrowUpRight width={17} height={17} />
            </a>
          </div>
        </div>
        <div className="product-shell paper-grid">
          {papers.map((paper) => (
            <article key={paper.title}>
              <div className="paper-preview"><Image src={paper.image} alt={`First page of ${paper.title}`} fill sizes="(max-width: 700px) 90vw, 380px" /></div>
              <span>{paper.label}</span><h3>{paper.title}</h3><p>{paper.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="whitepaper-stage">
        <div className="product-shell whitepaper-inner">
          <div>
            <p className="quiet-label quiet-label-blue">Go deeper</p>
            <h2>The full system.<br />No hand-waving.</h2>
            <p>Architecture, memory budgets, FPGA gates, risk register, and falsification criteria—documented for researchers, builders, and early believers.</p>
            <div className="stage-actions">
              <Link className="primary-action primary-action-light" href="/research">
                Read the whitepaper <OpenBook width={18} height={18} />
              </Link>
              <a className="secondary-action" href="/research/pocket-pet-ai-whitepaper.pdf" download>
                Download PDF <Download width={18} height={18} />
              </a>
            </div>
          </div>
          <div className="whitepaper-cover">
            <Image src="/product-v1/whitepaper/cover.png" alt="Cover of the Pocket Pet AI technical whitepaper" fill sizes="(max-width: 900px) 72vw, 430px" />
          </div>
        </div>
      </section>

      <footer className="product-footer">
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
