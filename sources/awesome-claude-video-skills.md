---
type: source
name: awesome-claude-video-skills
registry: awesome-claude-video-skills
url: https://github.com/zhuyansen/awesome-claude-video-skills
commit: "579887c"
read_on: 2026-11-19
counts: {entries: 526, pages: 0, waiting: 0, index_only: 64, deferred: 7, rejected: 455}
---

# awesome-claude-video-skills: what it gives RoboAI

A catalogue of 526 agent skills and tools that make or edit video, in ten sections (frameworks,
promos, explainers, editing, shorts, avatars, stories, motion graphics, scripts, music videos).
Most entries are social-media, advert and promo makers, so most are rejected. For the
[video track](../docs/plan.md#10-video-track) it gives one trial and five tools to watch:
HyperFrames as a renderer for CAD exploded views, three patterns for exploded views and
mechanisms (claude-animation-skills, a Blender explainer, Manim for kinematics), and two tools
for tutorial recordings and builders' footage. explainroo is in it already; video-director,
huashu-motion and earshot are not.

## How it was read

- Read at commit `579887c` (2026-11-18) on 2026-11-19, from a shallow clone: the README and
  `data/skills.json` (526 entries). Each entry is the GitHub repo `github.com/<entry>`;
  EverMind-AI/Raven points to its `skills/git-story-film` folder.
- The list is generated every 8 hours by its maintainer's Agent Skills Hub (agentskillshub.top),
  which also grades each entry for security, so it is partly self-promotion. It is CC0-1.0. No
  text in it is aimed at agents.
- Its "Which one to install" and "Tested end to end" tables (16 skills run on 2026-10-11) and
  "Made with Claude Opus 5.5" add no new entries. Its two related collections,
  opusvideo/awesome-claude-video (a showcase of finished videos) and
  TripoGrowthLab/awesome-opus-5-5-prompts (prompts for 3D scenes and games), are off topic and
  not counted.
- Every entry's last commit was read on 2026-11-19 with a blob-less shallow fetch. Two repos,
  nocodehack/make-short and nocodehack/nocodehack-roblox-engine, asked for credentials (deleted
  or private). 34 rejected entries had no commit since 2026-05-19. Licences of the six candidates
  were read from their LICENSE files; the others are GitHub's detection, as the list records it.
- The six candidates were checked in their own repos (last commit, licence, stars, Windows
  support, paid services, what the installer does) and are registered as `planned` or
  `watching`; their facts are in the registry notes.
- Researched on their own the same day, with registry entries: remotion-dev/skills and
  digitalsamba/claude-code-video-toolkit, both rejected (Remotion's licence needs a paid company
  licence for any for-profit firm of four or more people).
- Seven entries copy or derive from Vincentwei1021/video-shotcraft (rejected, not in this list):
  JohnChow90/video-shotcraft, syklayou-glitch/video-shotcraft, kingselyjoe/video-shotcraft-dsh,
  ChenShuo2004/cs-shotcraft-skill, dlazy-ai/ai-product-video,
  kiki-lgtm-dot/cinematic-product-promo-skill and erduo1998-cell/erduo-broll-loop-engineering.
- Name clashes: SallyRS/video-director is not the registered win4r/video-director, and
  alchaincyf/huashu-art-motion is a sibling of huashu-motion, not the same repo.
- Bangla narration: no local voice was found. Two leads are unchecked:
  lewislf/claude-code-video-studio uses OmniVoice (AGPL; Linux and an NVIDIA GPU), and
  marketcalls/story-telling uses Sarvam AI, a paid service for Indian languages.

## Pages made

| Entry | Page | Tier |
|---|---|---|

## Waiting for a page

<!-- Video tools get pages in wiki/tools/video/ when the video track adopts them. -->

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

## Index only

<!-- Tier C: useful to know, not worth registering. -->

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| 0xS4N4TG/kinetograph | Fast programmatic video engine for agents; alternative renderer; overlaps explainroo/HyperFrames | 2026-11-18 | Apache-2.0 |
| 0xsline/OpenChatCut | Local conversational editor with multi-track timeline; AGPL; overlaps MakeMyClip | 2026-11-12 | AGPL-3.0 |
| aaitor/skill-video-studio | Product videos from real browser capture; browser capture; overlaps explainroo record | 2026-11-19 | MIT |
| Aaryan-Kapoor/video-production-skill | Educational video pipeline with QC; overlaps explainroo + video-director | 2026-07-09 | MIT |
| adityaarsharma/youtube-marketing-skills | YouTube SEO, thumbnails, analytics MCP; for publishing the channel later | 2026-10-10 | MIT |
| Agentchengfeng/chengfeng-videocut-skills | Talking-head cutting agent (Chinese); popular cutter; overlaps explainroo cut | 2026-09-20 | Apache-2.0 |
| alchaincyf/huashu-art-motion | 35 art styles animated in code (huashu-motion's author); sibling of registered huashu-motion; art styles not needed | 2026-11-17 | MIT |
| AmadeusBio-ai/Molecular_Animation | Molecular science films in Blender; blender science-pipeline pattern | 2026-10-24 | Apache-2.0 |
| AmitSubhash/3brown1blue | Manim 3Blue1Brown-style generator and skill; manim alternative; last commit slowing | 2026-06-28 | MIT |
| Avijit07x/cursorcam | Agent clicks through a web app, zooms per click; web demos; overlaps agent-screenplay | 2026-10-23 | Apache-2.0 |
| bangtutorial/bang-motion | Browser motion graphics in one index.html; overlaps huashu-motion (HTML motion) | 2026-09-15 | MIT |
| Barty-Bart/motion-graphics | Motion graphics over talking-head footage (tested 4/4); talking-head focus; licence unclear | 2026-10-13 | other/unclear |
| brookejlacey/boring-tools | Edit-as-text with ffmpeg + whisper + Python; minimal transcript editing; overlaps explainroo cut | 2026-08-14 | MIT |
| cartesiancs/cartcut | Video editor built for agents; overlaps MakeMyClip | 2026-11-09 | MIT |
| cclank/lanshu-animated-architecture-diagram | Hand-drawn animated architecture diagrams; diagram animation for ROS 2 graphs | 2026-09-03 | MIT |
| DbgKinggg/plotbeat | HyperFrames chart-video templates; chart videos; overlaps explainroo charts | 2026-08-14 | MIT |
| diffusionstudio/lottie | Lottie animations from agents (tested 4/4); lottie for web/UI; not a video-track need | 2026-07-25 | MIT |
| echris6/motion-video-kit | Business video kit: critic loop, Three.js patterns, sound; critic loop + Three.js patterns; slow (21.8 min in the list's test) | 2026-10-14 | MIT |
| edotheDev/claude-video-kit | Agents to edit real footage and make motion films; footage editing with measured sound; overlap | 2026-10-15 | MIT |
| FavioVazquez/showtime | Local agent-directed video studio, no API keys; local all-rounder; overlaps explainroo | 2026-10-16 | MIT |
| feitangyuan/onetake | One-camera continuous motion films for launches; tested 4/4; promo focus overlaps huashu-motion; licence unclear | 2026-11-18 | other/unclear |
| FireRedTeam/FireRed-OpenStoryline | Intent-driven AI editing agent; large editing agent; overlaps explainroo cut | 2026-07-31 | Apache-2.0 |
| frankShan001/CutVoke | Local-first editor over MCP, Windows/macOS/Linux; cross-platform; overlaps MakeMyClip | 2026-11-19 | MIT |
| gquthier/autonomous-sop-video | Workflow to narrated tutorial with zooms and chapters; tutorial pattern; overlaps explainroo | 2026-10-15 | MIT |
| haiderfarooq3/khan-explainer | Khan-style pen-drawing explainers, local, free; whiteboard style; overlaps explainroo | 2026-10-11 | MIT |
| hassancs91/claude-youtube-editor | Talking head to YouTube video with Remotion visuals; builder talking-head videos; uploads to YouTube | 2026-11-05 | MIT |
| howseen-ai/claude-motion-design | Motion design in HTML + Playwright + ffmpeg; tested 4/4; overlaps huashu-motion; "caution" | 2026-10-02 | MIT |
| hughminhphan/motion-kit | Motion-designer timing rules for GSAP timelines; animation feel for HyperFrames/huashu-motion | 2026-11-04 | MIT |
| iart-ai/data-animation-skills | CSV to animated chart with exact numbers; accurate charts; overlaps explainroo charts | 2026-11-11 | MIT |
| iart-ai/explainer-video-skills | Narrated explainers and animated diagrams; animated-diagram skill; overlaps explainroo | 2026-11-11 | MIT |
| iart-ai/motion-design-skills | Motion design fundamentals (timing, type, colour); design guidance; overlaps video-director | 2026-11-11 | MIT |
| iart-ai/motion-skills | 56 motion skills in packs (Manim, data viz, WebGL, Remotion); broad vendor-run catalogue; its Manim and data-viz packs are worth a look | 2026-11-17 | MIT |
| iart-ai/youtube-video-skills | Audiograms and YouTube intros/outros; channel intro/outro | 2026-11-11 | MIT |
| isabellagreco1997/script-to-video | Script to word-synced explainer, local Kokoro; same approach as explainroo | 2026-09-06 | MIT |
| JimLiu/baocut | Agent editor: transcribe, subtitle, translate, dub; licence unclear; overlap | 2026-11-19 | other/unclear |
| Karnaf0katom/taskfilm | Local CLI for software-walkthrough tutorials; tutorial idea; overlaps explainroo record; "caution" | 2026-10-21 | MIT |
| kmilo93sd/agent-video-editor | Editing judgment + 128 CC0 sounds, 26 CC0 graphics; CC0 asset pack; overlaps earshot | 2026-10-04 | MIT |
| lazypay/Archscribe | Animated Excalidraw diagrams to GIF; diagram alternative | 2026-07-15 | MIT |
| lemomo-ai/lemo-opuscar | 99 code-made film styles with demo films; style library for a channel look; licence unclear | 2026-11-17 | other/unclear |
| leodavincs/kalem | Picks an engine per scene (Paper.js, PixiJS, HyperFrames, Three.js, Manim); multi-engine idea; licence unclear | 2026-11-06 | other/unclear |
| lewislf/claude-code-video-studio | Local studio: OmniVoice, MusicGen, HyperFrames, SDXL; multilingual local voice lead; Linux + NVIDIA only | 2026-11-13 | MIT |
| Lunamos/paper2video | Paper to 3B1B-style Remotion explainer; real-data animation pattern | 2026-10-24 | MIT |
| manoletre/explainer-video | Papers to ManimGL with local LFM2.5-Audio voice; local TTS alternative | 2026-11-11 | MIT |
| Mng-dev-ai/explainer-video | Topic to narrated explainer, local and free; overlaps explainroo | 2026-05-27 | MIT |
| Moessif/code-video-showcase | Beat-synced showcase videos in pure code (Canvas/Three.js, numpy score); code-only Three.js + synthesised score pattern | 2026-10-28 | MIT |
| Moh4696/cinematic-skill | One continuous camera over photos, maps, cards timed to voice; narrated cinematic style; overlaps explainroo | 2026-11-09 | MIT |
| mromidev/claude-blender-skills | Realistic Blender film workflows (drone, forest, car); blender bridge pattern; bridge runs any Python on localhost | 2026-10-25 | MIT |
| nolangz/pixel2motion | Raster logo to SVG animation; channel logo sting | 2026-08-21 | MIT |
| OnurGumus/codebase-video | Codebase to fact-checked narrated video; claim-verification pattern for robot explainers | 2026-10-28 | MIT |
| OpenMontageInc/OpenMontage | All-in-one agentic production system, 12 pipelines; overlaps explainroo; AGPL; list grades it "caution" | 2026-11-15 | AGPL-3.0 |
| oxygenframe/oxframe-sdk | Motion graphics as Rust code, native renderer; native deterministic renderer; early | 2026-10-27 | Apache-2.0 |
| PHANTOMTONYT/motion-design-skills | Five styles incl. 3D toy, system diagrams, data charts; system-diagram style; small | 2026-10-16 | MIT |
| pireel/pireel | Open editor over MCP: captions, cuts, NLE export; AGPL; overlaps MakeMyClip | 2026-11-16 | AGPL-3.0 |
| qualixar/brief2mp4 | Brief to checked MP4, 30 art forms incl. 3D products; 3D product forms; overlap | 2026-11-18 | MIT |
| SallyRS/video-director | HyperFrames directing skill (not the registered win4r one); name clash with registered video-director; promo focus | 2026-11-10 | MIT |
| Science-Prof-Robot/recursive-math-animator | Manim with manim-voiceover and scene versioning; manim + voice pattern; optional Gemini TTS | 2026-08-12 | MIT |
| smwbev/framewright | Short videos from one HTML file, frame as a pure function; deterministic-frame pattern; overlaps huashu-motion | 2026-09-26 | MIT |
| ssrajadh/paperview | Papers and codebases to explainers, local TTS; overlaps explainroo | 2026-06-16 | Apache-2.0 |
| staryone/motlab | Canvas scenes rendered with WebCodecs in headless Chrome; alternative renderer | 2026-11-18 | MIT |
| SunandBean/paper2video | arXiv paper to explainer (Three.js, local Kokoro); same voice stack as explainroo plus Three.js scenes | 2026-11-09 | MIT |
| Tejashmakwana/motionmaxxing | Motion-design taste rules that lift agent-made films; polish rules usable with any renderer; Apache-2.0 | 2026-10-06 | Apache-2.0 |
| vawe-hq/vawe | HTML page to MP4 framework; small HyperFrames/Remotion alternative | 2026-11-19 | Apache-2.0 |
| YKLovePython/halfsize | Compresses video to an exact size, VMAF check, MCP; delivery utility, not a video maker | 2026-11-19 | MIT |
| ythx-101/live-panel-skill | JSON to animated architecture diagram with flowing packets; fits animated ROS 2 node/topic graphs; WSL only on Windows | 2026-11-12 | MIT |

## Deferred

<!-- Registered candidates, with the video-track step that will try them. -->

| Entry | What it is | Phase | Registry |
|---|---|---|---|
| heygen-com/hyperframes | HTML + GSAP/Three.js compositions rendered to deterministic MP4; CLI, skills, catalogue | V3, exploded views | `hyperframes` (planned, trial) |
| MakeMyClip/editor | Local editor: silence/retake removal, transcript cuts, captions, NLE export | Builders' footage | `makemyclip-editor` (watching) |
| gmpetrov/agent-screenplay | Scripted, re-recordable screen recordings of web and desktop apps with zooms and callouts | ROS 2 tutorials | `agent-screenplay` (watching) |
| vincentsch/explainroo | Narrated explainers: Kokoro voice, Whisper timing, canvas renderer | V1, PID pilot | `explainroo` (planned, core) |
| sunxiayi/make-blender-education-video-skill | Fact-checked cinematic explainers in Blender with Kokoro narration | V3, if Three.js looks too plain | `make-blender-education-video-skill` (watching) |
| artemnovitckii/claude-animation-skills | Reel animation skills incl. /breakdown, a labelled 3D exploded view | V3, exploded views | `claude-animation-skills` (watching) |
| awesome-skills/manim-skill | Manim CE skill: scene authoring, preview, inspection; uv-pinned | Control explainers, after V1 | `manim-skill` (watching) |

## Rejected

| Entry | Why | Date |
|---|---|---|
| 022512db-netizen/rhythm-dancer-video | Off topic | 2026-11-19 |
| 0x68616F4C/auto-popsci | Abandoned (>6 months); no licence | 2026-11-19 |
| 0xS4N4TG/papercut-explainer | Social | 2026-11-19 |
| 10291124jcjc-dotcom/ancient-rap-battle | Paid services | 2026-11-19 |
| 10291124jcjc-dotcom/guiji-marble-video | No licence | 2026-11-19 |
| 10291124jcjc-dotcom/motion-reel | Ads | 2026-11-19 |
| 10291124jcjc-dotcom/xp-desktop-mv | No licence; "caution" | 2026-11-19 |
| 124zhe/xigua-msvideo-skill | Off topic | 2026-11-19 |
| 8533502-dev/deepseek-opus-motion-skill | Model-specific port | 2026-11-19 |
| aaksa/facecammaxxing | Social; licence unclear | 2026-11-19 |
| Abhinav-murugan1/Aria | Overlap | 2026-11-19 |
| abhinavshrivastava950/Montara | Early; AGPL; overlap | 2026-11-19 |
| AbubakrChan/product-launch-motion | Launch promos | 2026-11-19 |
| acelera-agency/html-animation | Overlap | 2026-11-19 |
| Acorn2/frame-loom | Overlap | 2026-11-19 |
| actionow-ai/vvv | Off topic | 2026-11-19 |
| adithya-s-k/manim_skill | Abandoned (>6 months); see awesome-skills/manim-skill | 2026-11-19 |
| adriiita/vertical-video-editing-skill | Social | 2026-11-19 |
| adunext/adu-motion-video | Points to an external template site; social | 2026-11-19 |
| Agentchengfeng/chengfeng-video-styles | Overlap | 2026-11-19 |
| AgriciDaniel/claude-gif | Abandoned (>6 months) | 2026-11-19 |
| AgriciDaniel/claude-shorts | Abandoned (>6 months) | 2026-11-19 |
| AgriciDaniel/lipnardo | Paid service; abandoned (>6 months) | 2026-11-19 |
| ahmdd4vd/MotionCraft | Overlap | 2026-11-19 |
| AIBiz-Automatyzacje/maszynka-do-shortsow | No licence | 2026-11-19 |
| aijiduonadegou/Paper-Cut | Style-specific | 2026-11-19 |
| AIPMAndy/Andy-Video-Skill | A list, not a tool | 2026-11-19 |
| AISEO-VirtualabDigital/mcp-video-editor | No licence | 2026-11-19 |
| AKMessi/vex | Vague; licence unclear | 2026-11-19 |
| AlbertPine/vibe-knowledge-video-director | No licence | 2026-11-19 |
| AlexAnsart/demo-studio | Paid TTS; overlap | 2026-11-19 |
| alexgreensh/anidoodle | Art; overlap | 2026-11-19 |
| Ali-Aria/aria-animator | Paid TTS | 2026-11-19 |
| aliangSSS/aliang-knowledge-video | Licence unclear | 2026-11-19 |
| alireza12t/foldline | macOS only | 2026-11-19 |
| Alisa0808/vox-director | Paid service | 2026-11-19 |
| alisadiq-ai/favstash-ai-video-editing-skills | Vendor service | 2026-11-19 |
| AllenAI2014/remotion-guofeng-starter | Licence unclear | 2026-11-19 |
| AmazingAng/ccvideo | Promos | 2026-11-19 |
| AmirSbss/spotlight | Social; overlap | 2026-11-19 |
| Anil-matcha/vox-ai-motion-graphics-generator | No licence; generative | 2026-11-19 |
| Anil-matcha/zack-d-films-ai-video-generator | Paid generative video; no licence | 2026-11-19 |
| AnmolChandiok/claude-after-effects-skill | Needs After Effects (paid) | 2026-11-19 |
| Anshgrover23/product-demo-playbook | No licence | 2026-11-19 |
| antropos17/chatgpt-gif-cinema | Off topic | 2026-11-19 |
| argus-metis/hermes-video-editing | Abandoned (>6 months); "caution" | 2026-11-19 |
| Arman-Luthra/aftr | Needs After Effects (paid) | 2026-11-19 |
| artemiimillier/skill-multik | Social | 2026-11-19 |
| artemnovitckii/claude-editing-skills | Social reels; licence unclear | 2026-11-19 |
| arthurkatcher/explainer-video | No licence | 2026-11-19 |
| AsadMoulviDev/reel-video | Off topic | 2026-11-19 |
| autoip/dreamfab | Service-bound; off topic | 2026-11-19 |
| axtonliu/video-illustrator | Overlaps explainroo | 2026-11-19 |
| ayushozha/AdobePremiereProMCP | Needs Premiere Pro (paid) | 2026-11-19 |
| bassimeledath/manimate | Abandoned (>6 months) | 2026-11-19 |
| BayramAnnakov/remotion-video-director | Abandoned (>6 months); no licence | 2026-11-19 |
| bbylw/hyperframes-cn | Duplicate of heygen-com/hyperframes | 2026-11-19 |
| beatra-ai/talking-avatar-video-skill | Avatars off topic | 2026-11-19 |
| beatra-ai/viral-video-remake-skill | Off topic | 2026-11-19 |
| beriki770-ship-it/code-animations | Overlap | 2026-11-19 |
| bestagentkits/motion-video-skill | Promo; overlap | 2026-11-19 |
| BetaVersionHQ/beta-version-blox-studio | Off topic | 2026-11-19 |
| BetaVersionHQ/beta-version-toon-studio | Off topic | 2026-11-19 |
| bishpls/animation-pipeline | No licence | 2026-11-19 |
| buildwithhanif/claude-animation-skill | Off topic | 2026-11-19 |
| BusyBee3333/animated-explainer-skills | Paid TTS; overlap | 2026-11-19 |
| BusyBee3333/viral-video-edit-skills | Music edits off topic | 2026-11-19 |
| BuzyOwl/song-video-director | Music off topic | 2026-11-19 |
| Cassette-Editor/oh-my-cassette | Montage; overlap | 2026-11-19 |
| cblain100-prog/motion-design-claude-code | Launch promos | 2026-11-19 |
| cclank/lanshu-create-ai-presenter-video | Avatars off topic; needs an avatar provider | 2026-11-19 |
| cclank/lanshu-html2video-skill | Overlap | 2026-11-19 |
| centraltowerlabs/diagram-tour | Abandoned (>6 months) | 2026-11-19 |
| chacha95/demo-video-creator | Launch promos | 2026-11-19 |
| Chamanrajragu/purffle-shorts | Social | 2026-11-19 |
| Changroro/code-video | Promo; off topic | 2026-11-19 |
| charlie947/motion-graphics-skills | Launch promos; overlap | 2026-11-19 |
| chenjun198711/book-video-generator | Off topic | 2026-11-19 |
| chenmisss/laoxu-video-script | Off topic | 2026-11-19 |
| chenqianshinian/music-mv-studio | Music off topic | 2026-11-19 |
| ChenShuo2004/cs-shotcraft-skill | Derivative of video-shotcraft (researched separately) | 2026-11-19 |
| chenyuxiaojin/cyxj-hyperframes | Overlap | 2026-11-19 |
| chenyuxiaojin/cyxj-remotion-starter | Same scaffold as vibe-motion/remotion-starter | 2026-11-19 |
| ChrisHKAI/ChrisHKAI-Video | Off topic | 2026-11-19 |
| chrisopal/narrated-video-studio | Overlaps explainroo; "caution" | 2026-11-19 |
| chuspeeism/dashi-animationstyle | Chinese-only; licence unclear | 2026-11-19 |
| CJ10110425/logo-intro | Small; overlaps pixel2motion | 2026-11-19 |
| clipugc/ClipUGC-CLI | Paid service | 2026-11-19 |
| cocolayuan/videoclip-AI-skill | Abandoned (>6 months) | 2026-11-19 |
| codepawl/creator-generalist | Vague scope; not a video-track need | 2026-11-19 |
| codewithsiddique-04/3d-video-studio | No licence; paid TTS | 2026-11-19 |
| codie1982/chorono-editor | Off topic | 2026-11-19 |
| coding-ax/docvideoer | Abandoned (>6 months) | 2026-11-19 |
| crawfordxx/paper-cut-video-skill | Paid TTS | 2026-11-19 |
| crawfordxx/xiaoma-studio | Promo style; overlap | 2026-11-19 |
| crimeacs/product-demo-director | Product demos; overlap | 2026-11-19 |
| Cuongyd196/remotion-cuongit-template | Social | 2026-11-19 |
| cymcymcymcym/notes-to-video | Abandoned (>6 months) | 2026-11-19 |
| d4niel-fr/shdw-video-editor | Early; AGPL | 2026-11-19 |
| dan2756/ReelForge | Social | 2026-11-19 |
| Dancan254/shenghua | Social; "caution" | 2026-11-19 |
| darrenli6/JJKoubo | Licence unclear | 2026-11-19 |
| dauletbekalim/motion-ui-videos | Promos | 2026-11-19 |
| david-d2c2/motion-promo-reels | Promos | 2026-11-19 |
| davidbfrogman/davecto-cutroom | macOS; no licence | 2026-11-19 |
| davidcervinka/vibe-editing | Promo/event films | 2026-11-19 |
| deenukhan/animation-styles | Overlap | 2026-11-19 |
| deenukhan/stick-figure-shorts | No licence | 2026-11-19 |
| deenukhan/story-animator | Paid TTS; off topic | 2026-11-19 |
| denyakortunov/family-travel-editor | Off topic | 2026-11-19 |
| derek-zhuolin/motion-skill | Overlap; licence unclear | 2026-11-19 |
| derrickgong87/demo-video-creation-skill | SaaS promos | 2026-11-19 |
| dev-isaacmello/extreme-motion-design | Overlaps registered tools | 2026-11-19 |
| digitalsamba/claude-code-video-toolkit | Researched on its own (registry `claude-code-video-toolkit`): Remotion and paid cloud models; uploads files to public hosts | 2026-11-19 |
| diko0071/remotion-video-skills | Product promos | 2026-11-19 |
| dillydog580/animate-roblox-characters | Off topic | 2026-11-19 |
| dlazy-ai/ai-product-video | Derivative of video-shotcraft (researched separately) | 2026-11-19 |
| doublesq97-ui/su-card-to-video | Minimal starter; overlap | 2026-11-19 |
| dovudhusan/viral-hook-reels-skill | Off topic | 2026-11-19 |
| Dryxio/effects-skill | Social | 2026-11-19 |
| dy-hashiqi/VibeDS-skill | No README description | 2026-11-19 |
| echoD886/dramacanvas-ai-filmmaking-mcp | Generative; off topic | 2026-11-19 |
| edenfunf/reelmimic | Off topic | 2026-11-19 |
| EGSECDA/vocaloid-style-mv-pipeline | Music videos off topic | 2026-11-19 |
| ekomen77/erko-ai-video-engine | Style-specific | 2026-11-19 |
| erduo1998-cell/erduo-broll-loop-engineering | Social B-roll; shotcraft derivative | 2026-11-19 |
| erduo1998-cell/video-script-builder | Overlap | 2026-11-19 |
| erduo1998-cell/vidmuse-video-creator | Vendor service | 2026-11-19 |
| eternityspring/reelbench-skills | Off topic | 2026-11-19 |
| EverMind-AI/Raven | Off topic | 2026-11-19 |
| every-app/video-skills | Product promos | 2026-11-19 |
| Fagan1024/smart-video-editor | Paid vision API | 2026-11-19 |
| fahmid-juboraj/reelforge | Social; licence unclear | 2026-11-19 |
| fantuan-lab/animated-sticker-studio | Off topic | 2026-11-19 |
| Fardeen26/launch-video-kit | Launch promos | 2026-11-19 |
| farming-labs/product-film-skill | Launch promos | 2026-11-19 |
| feicaiclub/knowledge-easy | No licence | 2026-11-19 |
| Felpborges/claude-video | Overlap | 2026-11-19 |
| fendouai/ViralForge | Off topic | 2026-11-19 |
| fernandokaraka/remotion-motion-graphics-skill | Overlap | 2026-11-19 |
| Finderchangchang/promo-video-skill | Promos | 2026-11-19 |
| fltman/infofilm | Paid services | 2026-11-19 |
| garycaogan/gary-pixel-diary | Off topic | 2026-11-19 |
| geekjourneyx/hyperframes-motion-director | Promo; AGPL; overlap | 2026-11-19 |
| generalizingai/shadowcast | Off topic | 2026-11-19 |
| ghost1412/shorts-generator | Social | 2026-11-19 |
| gloweaseco-leo/hyperdirector | Hermes-specific | 2026-11-19 |
| gnipbao/minimax-h3-video-reverse-skill | Generative | 2026-11-19 |
| gnipbao/story-to-handdrawn-video | Off topic | 2026-11-19 |
| GODGOD126/opus-5-5-86-styles-in-motion | No licence | 2026-11-19 |
| GordenSun/react-bits-video | Effects showcase; licence unclear | 2026-11-19 |
| GoRenku/studio | Film production; AGPL; off topic | 2026-11-19 |
| gorkem-bwl/onboarding-video-generator | Abandoned (>6 months) | 2026-11-19 |
| griffinwooldridge/talking-head-editor | Licence unclear | 2026-11-19 |
| GTAI-1/flow-mcp | Paid subscription; generative video; no licence | 2026-11-19 |
| GTKottman/mortiflix-oss | Overlaps explainroo; AGPL | 2026-11-19 |
| hacimertgokhan/geomotion | Off topic | 2026-11-19 |
| hahadu4520/newcut-video-clipping-skill | Social | 2026-11-19 |
| hahadu4520/vlog-cut | Abandoned (>6 months) | 2026-11-19 |
| haiderfarooq3/paper-reel | Social | 2026-11-19 |
| Hainrixz/editor-pro-max | Promo templates; licence unclear | 2026-11-19 |
| Hainrixz/motion-architect | Brand promos | 2026-11-19 |
| Hainrixz/video-editor-architect | Social; "caution" | 2026-11-19 |
| hamen/app-promo-reel | Promos | 2026-11-19 |
| hassancs91/claude-faceless-shorts-creator | Social; paid TTS | 2026-11-19 |
| haxzie/genmotion | No licence | 2026-11-19 |
| hdduytran/one-studio-skill | No licence | 2026-11-19 |
| hetpatel-11/Adobe_Premiere_Pro_MCP | Needs Premiere Pro (paid) | 2026-11-19 |
| HeyChengC/wallstreet-explainer | Off topic; licence unclear | 2026-11-19 |
| heygen-com/skills | Paid service | 2026-11-19 |
| hi-nikola/hand-drawn-explainer-video-nikola | Chinese-only style | 2026-11-19 |
| HibaBenzahra/HibAi-Editing-Studio | Social | 2026-11-19 |
| hildlabs/openrig-studio | Off topic | 2026-11-19 |
| holy-templar/static-to-video-ad | Paid service; ads | 2026-11-19 |
| holy-templar/vox-animated-ad-mcp | Paid service; AGPL | 2026-11-19 |
| howoneai/xiaolin-explainer-packaging | Imitates a creator; licence unclear | 2026-11-19 |
| hraness/slopcamera | Retired | 2026-11-19 |
| HRuiCcc/RuiC-motion-reel | Licence unclear | 2026-11-19 |
| hsynozdamar-byte/cinecode-studio | Off topic | 2026-11-19 |
| huaxialucaicaizi/opus5.5-video-skills- | No README description; "caution" | 2026-11-19 |
| hub-ki/video-generation | Product demos | 2026-11-19 |
| hubeiqiao/og-video-preview | Off topic | 2026-11-19 |
| huynhcongdac/story-video-skill | Off topic | 2026-11-19 |
| huypham85/app-3d-video-skill | macOS only; iOS promos | 2026-11-19 |
| Hype-yolo/claude-motion-skill | Promo motion; overlaps huashu-motion | 2026-11-19 |
| hypit-ai/hypit | Off topic (viral cloning, face swap); licence unclear | 2026-11-19 |
| i-afaqrashid/claude-animation-studio | Licence unclear | 2026-11-19 |
| iamajmeena/pro-motion-editor-skill | Licence unclear | 2026-11-19 |
| iart-ai/ad-video-skills | Ads | 2026-11-19 |
| iart-ai/ecommerce-video-skills | Off topic | 2026-11-19 |
| iart-ai/javascript-animation-skills | Overlap | 2026-11-19 |
| iart-ai/kinetic-typography-skills | Overlap | 2026-11-19 |
| iart-ai/map-animation-skills | Off topic | 2026-11-19 |
| iart-ai/text-message-video-skills | Off topic | 2026-11-19 |
| iart-ai/tiktok-video-skills | Social | 2026-11-19 |
| icytear-svg/podcast-to-video | No licence | 2026-11-19 |
| IdkwhatImD0ing/claude-music-videos | Single works | 2026-11-19 |
| imMamdouhaboammar/motion-graphics-skills | Brand films; licence unclear | 2026-11-19 |
| indieshade/video-director-workflow | Overlaps video-director | 2026-11-19 |
| inematds/skill-video-plan-editor | No licence | 2026-11-19 |
| intelligent-iterations/ii-content-engine | Abandoned (>6 months); uses browser cookies | 2026-11-19 |
| isaachang/motion-video-workflow | Social | 2026-11-19 |
| isaaclins/demo-video-skill | Paid TTS; licence unclear | 2026-11-19 |
| IskakovDamir/apple-motion | Promo style | 2026-11-19 |
| itwanger/one-minute-remotion | Overlap | 2026-11-19 |
| itwanger/vibe-science | Overlap | 2026-11-19 |
| jabbarlee/open-papertrail | macOS voice | 2026-11-19 |
| jackjls/jtxvideo-skill | Off topic | 2026-11-19 |
| Jadouminou/final-phase-lite | Small; overlaps explainroo preview | 2026-11-19 |
| jammaru/launch-video-craft | Launch promos | 2026-11-19 |
| Jane-xiaoer/paper-collage-ad-codex | Ads | 2026-11-19 |
| jaredcassoutt/vox-editorial | Style-specific; licence unclear | 2026-11-19 |
| jaxxchen003/book-video-factory | Off topic | 2026-11-19 |
| JDhruv14/line-art-animation | Character animation; off topic | 2026-11-19 |
| jdrurka/explainer-skill | Paid TTS | 2026-11-19 |
| jhartquist/claude-remotion-kickstart | Abandoned (>6 months) | 2026-11-19 |
| JimLiu/taohuayuan | A single work; no licence | 2026-11-19 |
| jincheng2026/jc-remotion-skills | Licence unclear | 2026-11-19 |
| jinjin1/scenewright | Overlap | 2026-11-19 |
| JJenglert1/remotion-claude-video | Abandoned (>6 months); no licence | 2026-11-19 |
| jjietay/clayducation | Style-specific | 2026-11-19 |
| JohnChow90/video-shotcraft | Duplicate of Vincentwei1021/video-shotcraft (researched separately) | 2026-11-19 |
| JohnHeibel/ClaudeAnimationBase | Cartoon; off topic | 2026-11-19 |
| JohnHeibel/PDoomVideo | A single work; no licence | 2026-11-19 |
| Johnson-Jia/video-clipforge | Social automation; off topic | 2026-11-19 |
| Joker-chichi/claude-mv-skill | Music videos; licence unclear | 2026-11-19 |
| jtydhr88/screenwriting-skills | Fiction writing; off topic | 2026-11-19 |
| JuneYaooo/capsule-cinema | Social templates; off topic | 2026-11-19 |
| JUNKDOGE-JOE/after-effects-mcp | Needs After Effects (paid) | 2026-11-19 |
| kajisho5/remotion-ffmpeg-skill | Overlap | 2026-11-19 |
| kakaxi12/vox-director-codex | No licence; paid TTS | 2026-11-19 |
| kangarooking/director-skills | Generative video; overlaps video-director | 2026-11-19 |
| kangarooking/promo-creator-skills | Abandoned (>6 months); promo | 2026-11-19 |
| Kanvis-chen/kanvis-video | Avatar/social focus | 2026-11-19 |
| Kappaemme-git/codex-video-short-maker-skill | Abandoned (>6 months) | 2026-11-19 |
| kasfulk/effectcraft-motion-skills | Overlap | 2026-11-19 |
| kelano86/what-if-animation | Paid TTS; off topic | 2026-11-19 |
| Kianzzz/xilo-opus-video | Promo; overlap | 2026-11-19 |
| kiki-lgtm-dot/cinematic-product-promo-skill | Derivative of video-shotcraft (researched separately) | 2026-11-19 |
| killkli/minimax-h3-colab-skill | Generative video; no licence | 2026-11-19 |
| Kimeur/motion-launch-videos | Launch promos | 2026-11-19 |
| kingselyjoe/video-shotcraft-dsh | Derivative of Vincentwei1021/video-shotcraft (researched separately) | 2026-11-19 |
| kjagsadvisors/keeran.ai | Marketing; off topic | 2026-11-19 |
| klsoen/opus-js-animations | Overlap | 2026-11-19 |
| krishnagoswami52/stickman-skill | Off topic | 2026-11-19 |
| krisyangdev/motionboard | Launch promos | 2026-11-19 |
| kurbaitaev/ghost-editor | Social reels | 2026-11-19 |
| kvrancic/oneshot-video | macOS | 2026-11-19 |
| Lanqiao-Luca/ai-video-marker | Off topic | 2026-11-19 |
| latent-variable/deep-learning-birthday | A single work | 2026-11-19 |
| leancoderkavy/premiere-pro-mcp | Needs Premiere Pro (paid) | 2026-11-19 |
| ledbetterljoshua/functional-emotions-video | A single work | 2026-11-19 |
| leosssvip-dot/remotion-ad-video-skill | Ads | 2026-11-19 |
| LetMeHappyCode/auto-video-agent | No licence | 2026-11-19 |
| Liamrjohnston/remotion-motion-graphics-skill | Overlap | 2026-11-19 |
| liangdabiao/story-handdrawn-remotion | No licence | 2026-11-19 |
| liangdabiao/story-handdrawn-video | No licence; generative | 2026-11-19 |
| liangdabiao/wechat-article-remotion | No licence | 2026-11-19 |
| liaojianquan9-source/ljq-broll-video-generator | Social B-roll | 2026-11-19 |
| lintsinghua/paint-mv-skills | Licence unclear | 2026-11-19 |
| lisamsung/agent-meme-forge | Off topic | 2026-11-19 |
| liuhaisi2026212-maker/motion-palette-15 | Licence unclear | 2026-11-19 |
| liuliu-66-create/ll-video-decomposer | Off topic | 2026-11-19 |
| liuliu-66-create/ll-video-edit | No licence | 2026-11-19 |
| liuliu-66-create/ll-video-motion | No licence | 2026-11-19 |
| liyue-aigc/xianxia-cinematic-video-director | No licence | 2026-11-19 |
| LordVayron/video-factory | Paid services | 2026-11-19 |
| louisedesadeleer/cut-video | Built for Apple Silicon | 2026-11-19 |
| luispablovillasenor-afk/shorts-animados-claude | Social | 2026-11-19 |
| lumian2015/opus-5-5-video-templates | Remakes others' videos; promo | 2026-11-19 |
| luminexlabs-io/antigravity-remotion-skill | Agent-specific | 2026-11-19 |
| Maartenlouis/remotion-ads | Abandoned (>6 months) | 2026-11-19 |
| mackswendhell/motion-code | No licence | 2026-11-19 |
| mad-helpers/motion-harness | Vague; early | 2026-11-19 |
| magichourhq/skills | Paid service | 2026-11-19 |
| marketcalls/story-telling | Paid APIs (Sarvam does Indian languages) | 2026-11-19 |
| mathruffian-dot/claude-motion-explainer-images | Overlap | 2026-11-19 |
| mathruffian-dot/claude-motion-explainer-video | Paid generative video | 2026-11-19 |
| Matteoikarieth96/cartoon-shorts-skill | Off topic | 2026-11-19 |
| Matteoikarieth96/whiteboard-video-skill | Overlap | 2026-11-19 |
| mattivilola/brag-codex | Clone; launch videos | 2026-11-19 |
| mattypark/Motion-graphics-skill | No licence | 2026-11-19 |
| mcdenil-skills/AutoMontage-Agent | Social | 2026-11-19 |
| MegaTroll222/VOX-COLLAGE-BROLL | Paid service | 2026-11-19 |
| memex-lab/product-launch-video-skill | Launch promos | 2026-11-19 |
| miguelcotrinaia/claude-skills-shorts-animados | Off topic | 2026-11-19 |
| mikelix/gstack-tutorial-5-agi-race-v2 | Example, not a tool | 2026-11-19 |
| mileson/chaojifeng-video-design | Overlaps video-director | 2026-11-19 |
| moguzbulbul/blueprint-animation | Off topic; licence unclear | 2026-11-19 |
| molkex/mcp-flow-google | Generative video on paid credits; licence unclear | 2026-11-19 |
| Monet-AI-Editor/Monet | Vague | 2026-11-19 |
| Mort1d/motion-graphics-skills | Showreels; licence unclear | 2026-11-19 |
| motalim-ai/motion-starter-kit | Social motion; overlap | 2026-11-19 |
| Mr-funny/hbg-douyin-code-explainer-video | No licence | 2026-11-19 |
| Mr-funny/hbg-life-simulation | Off topic | 2026-11-19 |
| mrieck/demoday-claude-plugin | Paid services | 2026-11-19 |
| mrpaidsocial/mrpaidsocial-video-editor-agent | No licence; paid TTS | 2026-11-19 |
| muayadjamal/flow-video-recorder | Paid TTS | 2026-11-19 |
| MuhammadaliMS/pixel-studio | Off topic | 2026-11-19 |
| murathany7/reel-studio | Marketing | 2026-11-19 |
| naive-kun/naive-video-skill | Social | 2026-11-19 |
| NarratorAI-Studio/narrator-ai-cli-skill | Wraps a commercial service; off topic | 2026-11-19 |
| Nealsun1993/talk-workbench | Vertical; overlap | 2026-11-19 |
| neelnanda-io/dont-go-quiet-on-me | A single work; licence unclear | 2026-11-19 |
| Neelshah1810/Claude-Video-Skills | Overlaps huashu-motion/explainroo | 2026-11-19 |
| neurolena1/video-effects-pack | Social; "caution" | 2026-11-19 |
| new-xp/ultrademo | Superseded by ultrademo-hq/ultrademo | 2026-11-19 |
| nexu-io/openmotion | Social/brand motion; overlaps huashu-motion | 2026-11-19 |
| ninestonelee/youtube-shorts-factory | Abandoned (>6 months) | 2026-11-19 |
| noamdorr/saas-product-demo-video | SaaS promos | 2026-11-19 |
| nocodehack/make-short | Repo unreachable (deleted or private) | 2026-11-19 |
| nocodehack/nocodehack-roblox-engine | Repo unreachable (deleted or private) | 2026-11-19 |
| nomicsadmin/editor-video-ia | macOS; licence unclear | 2026-11-19 |
| norahe0304-art/30x-video | Launch promos | 2026-11-19 |
| nxrskyaa/motionite | Overlap; licence unclear | 2026-11-19 |
| ocepkejepintu-droid/claude-launch | Launch promos; "caution" | 2026-11-19 |
| onuryildriim/claude-kurgu-atolyesi | Overlap | 2026-11-19 |
| op7418/guizang-product-video-skill | Product promos; AGPL | 2026-11-19 |
| ops120/video-recap-skills-plus | Off topic; "caution" | 2026-11-19 |
| opus-pro/opusclip-video-tools | Commercial vendor; no licence | 2026-11-19 |
| ouerf-man/kinetic-editorial-skill | No licence | 2026-11-19 |
| patraxo/ltx2-vidgen-skill | Paid GPU cloud; generative | 2026-11-19 |
| patryk-penczek/ship-video | Launch promos | 2026-11-19 |
| paullabs/espaco-em-codigo | Own licence with mandatory watermark | 2026-11-19 |
| pedroxcardoso/maquina-cortes-gta | Off topic | 2026-11-19 |
| Phantomlau3674/voxstylehub-steven | Style-specific | 2026-11-19 |
| Phucanh-MRT/mrtkeyword | No licence | 2026-11-19 |
| pjecuacion/script-to-video-skill | Abandoned (>6 months) | 2026-11-19 |
| PoetCoderJun/MotionTalk | Licence unclear | 2026-11-19 |
| precious112/demo-director | Product demos | 2026-11-19 |
| puntorigen/avatar-skills | Cloud service | 2026-11-19 |
| pyang5166/gbro-collage-broll | Paid generative | 2026-11-19 |
| pyang5166/gbro-collage-info | Style-specific | 2026-11-19 |
| pycodebr/heditor | Social | 2026-11-19 |
| qingyunAGI/qingyun-cine-skill | No licence | 2026-11-19 |
| rafiimanggala/paper-collage-skill | Style-specific | 2026-11-19 |
| rahlquist/hermes-video-toolchain | Hermes-specific; "caution" | 2026-11-19 |
| RahmanBuildsAI/ravyn-reel-kit | Not-for-resale terms; licence unclear | 2026-11-19 |
| RajaskaJanuardani/motion-craft | Promo motion; overlap | 2026-11-19 |
| reedodev/explainer-studio | Overlap | 2026-11-19 |
| remotion-dev/skills | Researched on its own (registry `remotion-skills`): Remotion License | 2026-11-19 |
| resemble-ai/remotion-resemble-skill | Abandoned (>6 months); paid TTS | 2026-11-19 |
| revfactory/showreel | Paid TTS | 2026-11-19 |
| riffkit/skill | Vendor service | 2026-11-19 |
| rjmahesh/ui-redline-walkthrough | UI design reviews; off topic | 2026-11-19 |
| rock3r/cav | Needs the Cavalry app | 2026-11-19 |
| rocketmandrey/stickman-director | Google service | 2026-11-19 |
| rocksstarcode/hyperframes-video-polish | Small add-on | 2026-11-19 |
| RohanRatwani/explainer-video-opus-5.5 | 2 stars; overlap | 2026-11-19 |
| RoverEva/eva-video-style | Social | 2026-11-19 |
| rtadewald/agent-video-editor | No licence | 2026-11-19 |
| runesleo/claude-video-kit | Vertical; overlap | 2026-11-19 |
| Samin12/samin-reel-engine-plugin | Social; licence unclear | 2026-11-19 |
| samuelstroschein/opus-video-generator | Launch promos | 2026-11-19 |
| sanskarprajapati/parallax-doc | Off topic | 2026-11-19 |
| santmun/video-vox | No licence | 2026-11-19 |
| sepi2p/research-explainer-skill | Overlap; "caution" | 2026-11-19 |
| sevenevesai/riso-windowseat | Art films | 2026-11-19 |
| shaderera/shaderera | Ads | 2026-11-19 |
| sharon-laicc/viral-video-decomposer | Off topic | 2026-11-19 |
| shasshhaank/ClipIt | Social | 2026-11-19 |
| Shugar86/vids-studio | Google Workspace service | 2026-11-19 |
| shuyicc/MathLens | Abandoned (>6 months); no licence | 2026-11-19 |
| siegerts/skill-canvas-video | Abandoned (>6 months) | 2026-11-19 |
| skailabinfo/claude-video-harness | Social | 2026-11-19 |
| smit-vanani/claude-promo-video | Promos | 2026-11-19 |
| social-media-skills/remotion-shorts-skill | Social | 2026-11-19 |
| SpaceZephyr/map-motion | China map service | 2026-11-19 |
| SpeedPainterOrg/explainer-video | No licence | 2026-11-19 |
| squall01337/mixamo-llm-mocap | Character mocap; off topic; licence unclear | 2026-11-19 |
| STARDUSTLC666/dsh-remotion | Tied to DeepSeek Harness | 2026-11-19 |
| sub-level/marketing-videos | Marketing | 2026-11-19 |
| sudadom/arabic-motion-graphics-skill | Off topic | 2026-11-19 |
| suiyang-meta/sui-motion-graphic-reel | Social; CC-BY | 2026-11-19 |
| sukai213/bilibili-ai-video | No licence | 2026-11-19 |
| suntay44/motionable | macOS; licence unclear | 2026-11-19 |
| Sunwood-ai-labs/hyperframes-motion-reel-skill | Showreels | 2026-11-19 |
| superyhee/hypr-video-skills | Abandoned (>6 months); no licence | 2026-11-19 |
| surajshetty3416/demo-video-skill | Web demos; overlaps agent-screenplay | 2026-11-19 |
| SyanChen7/dancing-notes | Music off topic | 2026-11-19 |
| SyedBahjat/claude-stickman-shorts | Off topic | 2026-11-19 |
| syklayou-glitch/video-shotcraft | Duplicate of Vincentwei1021/video-shotcraft (researched separately) | 2026-11-19 |
| synchronicity-labs/skills | Paid API | 2026-11-19 |
| syydaniel/kazi | Licence unclear; overlap | 2026-11-19 |
| talsiach/take-one | Already rejected 2026-11-12 (registry `take-one`): overlaps huashu-motion | 2026-11-19 |
| taylorzhou16/video-gen | Abandoned (>6 months); no licence | 2026-11-19 |
| Teseife/diffusion-studio-codex | Small; vendor-tied | 2026-11-19 |
| TheMarco/claude-music-video | Music off topic | 2026-11-19 |
| TheNoumanDev/zero-dollar-studio | Social | 2026-11-19 |
| threeaus/creator-style-kit | Social | 2026-11-19 |
| threerocks/sweety-statechart-video | Style-specific | 2026-11-19 |
| thuann-vn/claude-3d-animated-shorts | Licence unclear | 2026-11-19 |
| timscheuerai/launch-video-kit | Launch promos | 2026-11-19 |
| tmakersas/revid-skills | Paid service; social | 2026-11-19 |
| tmoody1973/pasteup | Style-specific | 2026-11-19 |
| toufuim/personal-ip-brand-intro-skill | Off topic | 2026-11-19 |
| trunghaiy/appshot | Off topic | 2026-11-19 |
| TryWorld2026/paper-algorithm | Social | 2026-11-19 |
| Tu-Zhenzhao/pocketworld | Off topic | 2026-11-19 |
| tugrawork-creator/saas-motion-kit | SaaS promos | 2026-11-19 |
| TurkiHassan/arabic-launch-video | Ads | 2026-11-19 |
| tuzhechen2005/opus-video-skills | Licence unclear | 2026-11-19 |
| UgurKeskekci/claude-video-kit | Licence unclear | 2026-11-19 |
| unclejobs-ai/motion-video-skill | Overlap | 2026-11-19 |
| undsky/doudou-remotion-whiteboard-skill | Licence unclear | 2026-11-19 |
| Upload-Post/avatar-mix | Paid service | 2026-11-19 |
| useapi/muse-api | Third-party API wrapper | 2026-11-19 |
| V413havai/vaibhav-video-editor | Social | 2026-11-19 |
| vakovalskii/nd-video-studio | Vendor models | 2026-11-19 |
| VasiniDevi/motion-skills | Abandoned (>6 months); no licence | 2026-11-19 |
| vibe-motion/remotion-code-motion-explainer | Overlap | 2026-11-19 |
| vibe-motion/remotion-starter | Remotion scaffold; overlap | 2026-11-19 |
| vibe-motion/skills | No licence | 2026-11-19 |
| Vibha-Ramprakash/claude-video-effects | Social effects; licence unclear | 2026-11-19 |
| video-db/skills | Needs VideoDB cloud | 2026-11-19 |
| vincentventalon/claude-code-video-editing-skill | Grab bag | 2026-11-19 |
| welingtondesosa/video-motion | Brand promos; licence unclear | 2026-11-19 |
| wendymardigian-prog/Editor-IA-Pro | Licence unclear | 2026-11-19 |
| WhiteTowerAI/cut-as-code | Social clipping | 2026-11-19 |
| Win-Hao/music-mv | Music videos off topic | 2026-11-19 |
| wocha-xiaoli/video-shot-analysis-feishu | Abandoned (>6 months) | 2026-11-19 |
| WoYun520/gif-factory | Off topic | 2026-11-19 |
| wshuyi/remotion-video-skill | Abandoned (>6 months); no licence | 2026-11-19 |
| ww-w-ai/super-video-agent | Source-available, not open licence | 2026-11-19 |
| wyuzhi/qisi-video-remix | Off topic | 2026-11-19 |
| wzslr321/fixtape | Off topic | 2026-11-19 |
| xdis/opus-video-studio | macOS; licence unclear | 2026-11-19 |
| Xiangyu-CAS/rea-capcut | Clone of a commercial app; legal risk | 2026-11-19 |
| xinyiqin/X2V-AI-Images-Videos-skill | Abandoned (>6 months); cloud API | 2026-11-19 |
| xsourabhsharma/remotion-marketing-video-skill | Abandoned (>6 months) | 2026-11-19 |
| XuHo-IT/Content-Agent-Kit | Off topic | 2026-11-19 |
| y-wi/horizon-montage-generic | Social | 2026-11-19 |
| YahyaLendani/motionbrief-claude-skills | Promo; "caution" | 2026-11-19 |
| yammaku/typewriter-video | Abandoned (>6 months); licence unclear | 2026-11-19 |
| YanKaFei/ascii-h3-director | Generative | 2026-11-19 |
| YeJe-cpu/SeeCut | Social; licence unclear | 2026-11-19 |
| yenceesanjeev/2d-character-sketch | Off topic; "caution" | 2026-11-19 |
| yerinsabraham/video-edit-skill | Social | 2026-11-19 |
| YIAN6557/eian-riso-broll | Licence unclear | 2026-11-19 |
| ymybxx/SoloMCN | Social | 2026-11-19 |
| Yuuhann1999/agent-storyboard | Generative storyboards | 2026-11-19 |
| yuwenbin121/book-video-production-skill | Off topic | 2026-11-19 |
| zakariaf/cinecode | Off topic | 2026-11-19 |
| Zane-0x5a/remotion-director | Promo; overlap | 2026-11-19 |
| zenitlab/video-as-code | Off topic | 2026-11-19 |
| zenstory-ai/video-recap-skills | Recap genre; off topic | 2026-11-19 |
| zhenwusw/orca-motion-skill | Overlap | 2026-11-19 |
| zhouyuechuan2025-ui/aipacking | Social | 2026-11-19 |
| ZiadAbdelkarim/beat-synced-edit | Music edits; off topic | 2026-11-19 |
| ZLHad/OpenVideoHarness | Overlaps explainroo + video-director | 2026-11-19 |
| zlong6943-commits/football-prediction-avatar-video | Off topic; no licence | 2026-11-19 |
| znyupup/ai-video-editing-skill | Abandoned (>6 months) | 2026-11-19 |
| znyupup/knowledge-explainer-skill | Abandoned (>6 months) | 2026-11-19 |
| zoglmk/codex-video-pipeline | Social | 2026-11-19 |
| zz41354899/mografy | Overlap; "caution" | 2026-11-19 |
