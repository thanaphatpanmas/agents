# Agent Setup

> **Last updated:** 2026-11-06 Asia/Bangkok (UTC+07:00)

`~/.agents` คือที่เก็บหลัก (`npx skills` ลง skill ที่นี่) Claude ใช้ symlink ใน `~/.claude/skills` ส่วนคอลัมน์ Codex ตรวจเฉพาะ `~/.codex/skills` (แถว AGENTS.md ตรวจ `~/.codex/AGENTS.md`): ❌ = ไม่มีไฟล์/symlink (ที่ถูกต้อง), ✅ = มี symlink หลุดเข้ามา ทั้งที่ Codex เห็น skill ผ่าน `~/.agents/skills` เองอยู่แล้ว

## Instruction file

แยก 2 ระดับ: Global ใช้กับทุกโปรเจกต์, Project อยู่ใน repo และใช้เฉพาะโปรเจกต์นั้น

### Global

- **Repo**: `~/Development/Projects/agents/AGENTS.md` — ไฟล์จริง (ต้นฉบับ)
- **Agents**: `~/.agents/AGENTS.md` — symlink → ต้นฉบับใน repo
- **Claude**: `~/.claude/CLAUDE.md` — symlink → ต้นฉบับใน repo
- **Codex**: `~/.codex/AGENTS.md` — symlink → ต้นฉบับใน repo

แก้ที่ `AGENTS.md` ใน repo ไฟล์เดียว ทั้งสามที่จะเปลี่ยนตามอัตโนมัติ

### Project

- `AGENTS.md`: กฎการทำงานของ agent: อ่านอะไรก่อนแก้, ใช้ skill ไหน, คำสั่ง verify, วิธีอัปเดตเอกสาร
- `CLAUDE.md`: มีแค่ `@AGENTS.md` เพื่อให้ Claude Code อ่านไฟล์เดียวกับ agent อื่น
- `ARCHITECTURE.md`: โครงสร้าง package/module, ที่วางไฟล์, data flow, i18n ownership, API naming, มาตรฐาน UI
- `DESIGN.md`: token และสเปกภาพของดีไซน์ (ส่วนบน = ของที่ import มา, ส่วนล่าง = override ของโปรเจกต์)
- `docs/*.md`: เอกสารเฉพาะเรื่อง เช่น `overview.md`, `date-time.md`, `tech-stack.md` อ่านเมื่อแตะงานนั้น
- `.agents/skills/*/SKILL.md`: ขั้นตอนเฉพาะงาน เช่น สร้าง module, reports, permissions

## Skills (`~/.agents/skills`)

### Sync และ Token

- **Tokens เริ่มต้น**: name + description ที่ agent โหลดทุก session
- **Tokens เมื่อเรียกใช้**: `SKILL.md` ทั้งไฟล์ โหลดเมื่อ skill ถูกเรียก (ไม่รวม references ที่อ่านเพิ่มตามขั้นตอน)
- นับด้วย o200k_base (ประมาณ)
- `grill-me`, `to-spec`, `to-tickets`, `setup-matt-pocock-skills`, `story` ตั้ง `disable-model-invocation: true` ไว้: Claude ไม่โหลด description ของ 5 ตัวนี้ตอนเริ่ม session และเรียกได้เฉพาะตอนพิมพ์ `/ชื่อ` ตัวเลขในตารางยังนับตามวิธีเดิม

<table>
  <thead>
    <tr><th>Skill</th><th>Agents</th><th>Claude</th><th>Codex</th><th>ลิงก์ติดตั้ง</th><th>Tokens เริ่มต้น</th><th>Tokens เมื่อเรียกใช้</th></tr>
  </thead>
  <tbody>
    <tr><th colspan="7" align="left">Instruction file</th></tr>
    <tr><td>AGENTS.md</td><td>✅ (symlink)</td><td>✅ (symlink)</td><td>✅ (symlink)</td><td><a href="https://github.com/thanaphatpanmas/agents/blob/main/AGENTS.md">AGENTS.md</a></td><td>857</td><td>—</td></tr>
    <tr><th colspan="7" align="left">วางแผนและจัดการงาน</th></tr>
    <tr><td>grill-me</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mattpocock/skills/grill-me">grill-me</a></td><td>27</td><td>36</td></tr>
    <tr><td>grilling</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mattpocock/skills/grilling">grilling</a></td><td>49</td><td>437</td></tr>
    <tr><td>to-spec</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mattpocock/skills/to-spec">to-spec</a></td><td>43</td><td>632</td></tr>
    <tr><td>to-tickets</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mattpocock/skills/to-tickets">to-tickets</a></td><td>68</td><td>1,270</td></tr>
    <tr><td>setup-matt-pocock-skills</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mattpocock/skills/setup-matt-pocock-skills">setup-matt-pocock-skills</a></td><td>63</td><td>1,873</td></tr>
    <tr><td>story</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thanaphatpanmas/agents/tree/main/skills/story">story</a></td><td>115</td><td>2,445</td></tr>
    <tr><td>commit</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thanaphatpanmas/agents/tree/main/skills/commit">commit</a></td><td>116</td><td>1,940</td></tr>
    <tr><td>pull-request</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thanaphatpanmas/agents/tree/main/skills/pull-request">pull-request</a></td><td>115</td><td>1,581</td></tr>
    <tr><td>workload</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thanaphatpanmas/agents/tree/main/skills/workload">workload</a></td><td>148</td><td>2,043</td></tr>
    <tr><td>short-notes</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thanaphatpanmas/agents/tree/main/skills/short-notes">short-notes</a></td><td>148</td><td>1,032</td></tr>
    <tr><th colspan="7" align="left">ออกแบบและพัฒนา Frontend</th></tr>
    <tr><td>design-taste-frontend</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/Leonxlnx/taste-skill">taste-skill</a></td><td>199</td><td>5,507</td></tr>
    <tr><td>impeccable</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/pbakaus/impeccable">impeccable</a></td><td>143</td><td>2,637</td></tr>
    <tr><td>modern-web-guidance</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/googlechrome/modern-web-guidance/modern-web-guidance">modern-web-guidance</a></td><td>226</td><td>1,864</td></tr>
    <tr><td>typescript-magician</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mcollina/skills/typescript-magician">typescript-magician</a></td><td>123</td><td>1,050</td></tr>
    <tr><td>vercel-react-best-practices</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices">vercel-react-best-practices</a></td><td>85</td><td>1,764</td></tr>
    <tr><td>vercel-composition-patterns</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/vercel-labs/agent-skills/vercel-composition-patterns">vercel-composition-patterns</a></td><td>75</td><td>626</td></tr>
    <tr><th colspan="7" align="left">ฐานข้อมูล</th></tr>
    <tr><td>supabase-postgres-best-practices</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices">supabase-postgres-best-practices</a></td><td>202</td><td>707</td></tr>
    <tr><th colspan="7" align="left">คุณภาพ ประสิทธิภาพ และ SEO</th></tr>
    <tr><td>best-practices</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://officialskills.sh/addyosmani/skills/best-practices">best-practices</a></td><td>65</td><td>2,990</td></tr>
    <tr><td>performance</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://officialskills.sh/addyosmani/skills/performance">performance</a></td><td>62</td><td>3,291</td></tr>
    <tr><td>seo</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://officialskills.sh/addyosmani/skills/seo">seo</a></td><td>59</td><td>3,234</td></tr>
    <tr><th colspan="7" align="left">Debug ทดสอบ และวิเคราะห์ระบบ</th></tr>
    <tr><td>debug-mantra</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thananon/9arm-skills/blob/main/skills/engineering/debug-mantra/SKILL.md">debug-mantra</a></td><td>117</td><td>1,104</td></tr>
    <tr><td>tdd</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mattpocock/skills/tdd">tdd</a></td><td>46</td><td>774</td></tr>
    <tr><td>codebase-design</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mattpocock/skills/codebase-design">codebase-design</a></td><td>71</td><td>1,349</td></tr>
    <tr><td>verification-before-completion</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/obra/superpowers/tree/main/skills/verification-before-completion">verification-before-completion</a></td><td>59</td><td>854</td></tr>
    <tr><td>playwright-cli</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/microsoft/playwright-cli/tree/main/skills/playwright-cli">playwright-cli</a></td><td>32</td><td>3,760</td></tr>
    <tr><td>reverse-engineer-anything</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/morluto/rea">REA</a></td><td>100</td><td>8,425</td></tr>
    <tr><th colspan="7" align="left">ค้นหาเอกสาร</th></tr>
    <tr><td>find-docs</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/upstash/context7/find-docs">find-docs</a></td><td>187</td><td>1,714</td></tr>
    <tr><th colspan="7" align="left">จัดการและสร้าง skill</th></tr>
    <tr><td>find-skills</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/vercel-labs/skills/find-skills">find-skills</a></td><td>80</td><td>1,303</td></tr>
    <tr><td>skill-creator</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/anthropics/skills/skill-creator">skill-creator</a></td><td>79</td><td>7,241</td></tr>
    <tr><th colspan="7" align="left">รวม</th></tr>
    <tr><td colspan="5">รวม skills 29 ตัว</td><td>2,902</td><td>—</td></tr>
    <tr><td colspan="5">ข้อความครอบ AGENTS และ mapping path</td><td>31</td><td>—</td></tr>
    <tr><th colspan="5" align="left">รวมทั้งหมด (ประมาณ, o200k_base)</th><th>3,790</th><th>—</th></tr>
  </tbody>
</table>

### การใช้งาน

พิมพ์ `/ชื่อ-skill` เพื่อเรียกได้แน่นอน คำอื่นในคอลัมน์ "ทำงานเมื่อ" แค่ช่วยให้ agent เลือก skill นั้นเอง (ดูจาก description ไม่ใช่จับ keyword ตรงตัว)

<table>
  <thead>
    <tr><th>Skill</th><th>ทำอะไร</th><th>ทำงานเมื่อ</th></tr>
  </thead>
  <tbody>
    <tr><th colspan="3" align="left">วางแผนและจัดการงาน</th></tr>
    <tr><td>grill-me</td><td>สัมภาษณ์เป็นรอบจน plan หรือ story ชัด (เรียก <code>grilling</code> ให้เอง)</td><td><code>/grill-me</code> เท่านั้น</td></tr>
    <tr><td>grilling</td><td>ถามเป็นรอบ ทุกคำถามมีคำตอบที่แนะนำ หาข้อเท็จจริงในโค้ดเองผ่าน subagent จนไม่เหลือเรื่องที่ต้องเดา</td><td><code>/grilling</code>, พูดว่า &quot;grill&quot;, ขอให้ซักแผนหรือไอเดีย</td></tr>
    <tr><td>to-spec</td><td>เขียน spec จากที่คุยกันมา ร่าง seam ให้ยืนยัน แล้วลง issue tracker</td><td><code>/to-spec</code> เท่านั้น</td></tr>
    <tr><td>to-tickets</td><td>แตก spec หรือแผนเป็น ticket แบบ vertical slice พร้อมลำดับที่ต้องรอกัน แล้วลง issue tracker</td><td><code>/to-tickets</code> เท่านั้น</td></tr>
    <tr><td>setup-matt-pocock-skills</td><td>ตั้งค่า repo ให้ <code>to-spec</code> และ <code>to-tickets</code>: issue tracker (GitHub, GitLab หรือไฟล์ local), label และที่เก็บเอกสาร domain</td><td><code>/setup-matt-pocock-skills</code> เท่านั้น รันครั้งเดียวต่อ repo</td></tr>
    <tr><td>story</td><td>พา spec จาก <code>to-spec</code> (หรืองานแก้เล็กๆ) ไปจนเปิด PR: เติม acceptance criteria ให้ E2E agent กับ Dev agent ทำพร้อมกัน ให้ Security agent ตัวใหม่หาช่องโหว่ ถ่าย screenshot ตาม criteria แล้ว commit + PR ทีละกลุ่ม ticket (ขั้นตอนอยู่ใน <code>FLOW.md</code>)</td><td><code>/story #&lt;issue&gt;</code> หรือ <code>/story &lt;สิ่งที่จะแก้&gt;</code> เท่านั้น</td></tr>
    <tr><td>commit</td><td>stage ทุกไฟล์ใน repo ปัจจุบันหรือโปรเจกต์ที่ระบุ commit แบบ Conventional Commits จาก diff แล้วให้เลือก commit อย่างเดียวหรือ commit + push</td><td><code>/commit</code>, &quot;commit and push&quot;, สั่ง commit/push เป็นภาษาไหนก็ได้</td></tr>
    <tr><td>pull-request</td><td>เปิดหรืออัปเดต PR (GitHub) / MR (GitLab รวม self-hosted) ของ branch ปัจจุบัน เลือก base จากผัง commit (main, dev, branch แม่ของ stacked) เขียนชื่อแบบ Conventional Commits และคำอธิบายจากทุก commit แล้วถามก่อนสร้าง (ต้องมี <code>gh</code>/<code>glab</code>)</td><td><code>/pull-request</code>, เปิด PR, สร้าง MR, ขอ merge, ส่งรีวิว</td></tr>
    <tr><td>workload</td><td>สรุป git commit ตามช่วงวันที่เป็น workload รายสัปดาห์ เติมให้ครบวันละ 8 ชม.</td><td><code>/workload</code>, ลงเวลา/ลงงาน/สรุปงานประจำสัปดาห์, ส่ง week ที่มีช่อง <code>[]</code> ว่าง</td></tr>
    <tr><td>short-notes</td><td>เขียน/แก้โน้ตส่วนตัว Markdown สไตล์ bullet + code เลือกภาษาไทย/อังกฤษ และระดับ brief/medium/detailed</td><td><code>/short-notes</code>, ขอจด/บันทึก/สรุปลงโน้ต, เพิ่มหรือเขียนโน้ต .md เดิมใหม่</td></tr>
    <tr><th colspan="3" align="left">ออกแบบและพัฒนา Frontend</th></tr>
    <tr><td>design-taste-frontend</td><td>สร้างเว็บบริษัท สินค้า หรือร้านค้าไม่ให้ดู generic (v2.5): เขียน copy ก่อน วางหน้าเป็นจอ สุ่ม palette และ hero ด้วย script แล้วตรวจใน headless Chrome (ต้องมี Node 22+ และ Chrome) ไม่ครอบคลุม dashboard/หน้าแอปแล้ว (ใช้ <code>impeccable</code>)</td><td><code>/design-taste-frontend</code>, สร้าง/รีดีไซน์ landing page, เว็บบริษัท สินค้า ร้านค้า SaaS หรือเกม, บอกว่าหน้าดู generic/&quot;AI-made&quot;</td></tr>
    <tr><td>impeccable</td><td>ออกแบบและปรับ UI: layout, typography, สี, motion, UX copy, accessibility และ responsive</td><td><code>/impeccable init</code>, <code>/impeccable audit</code>, <code>/impeccable critique</code>, <code>/impeccable polish</code></td></tr>
    <tr><td>modern-web-guidance</td><td>แนวทาง HTML/CSS/JS ฝั่ง client แบบใหม่ จาก Google Chrome</td><td><code>/modern-web-guidance</code>, งาน UI, layout, scroll/animation, web API, ฟอร์ม, accessibility</td></tr>
    <tr><td>typescript-magician</td><td>generic type, ลบ <code>any</code>, type guard, แก้ compiler error</td><td><code>/typescript-magician</code>, ถามเรื่อง TypeScript type, generic, ลบ <code>any</code>, type error</td></tr>
    <tr><td>vercel-react-best-practices</td><td>ปรับ performance ของ React/Next.js</td><td><code>/vercel-react-best-practices</code>, เขียน/รีวิว/refactor React หรือ Next.js</td></tr>
    <tr><td>vercel-composition-patterns</td><td>แก้ component ที่มี boolean prop เยอะ ด้วย compound component, render props, context</td><td><code>/vercel-composition-patterns</code>, props เยอะเกิน, ทำ component library, วางโครง component</td></tr>
    <tr><th colspan="3" align="left">ฐานข้อมูล</th></tr>
    <tr><td>supabase-postgres-best-practices</td><td>ออกแบบ schema, migration, RLS, index, แก้ query ช้า</td><td><code>/supabase-postgres-best-practices</code>, งาน Postgres ทุกอย่าง แม้แก้คอลัมน์เดียว</td></tr>
    <tr><th colspan="3" align="left">คุณภาพ ประสิทธิภาพ และ SEO</th></tr>
    <tr><td>best-practices</td><td>ตรวจ/ปรับโค้ดเว็บตาม best practice ด้าน security, compatibility, คุณภาพโค้ด</td><td><code>/best-practices</code>, &quot;security audit&quot;, &quot;modernize code&quot;, &quot;check for vulnerabilities&quot;</td></tr>
    <tr><td>performance</td><td>เพิ่มความเร็วเว็บ ลดเวลาโหลด</td><td><code>/performance</code>, &quot;speed up my site&quot;, &quot;performance audit&quot;, เว็บโหลดช้า</td></tr>
    <tr><td>seo</td><td>ปรับ meta tag, structured data, sitemap</td><td><code>/seo</code>, &quot;improve SEO&quot;, &quot;fix meta tags&quot;</td></tr>
    <tr><th colspan="3" align="left">Debug ทดสอบ และวิเคราะห์ระบบ</th></tr>
    <tr><td>debug-mantra</td><td>วินัย debug 4 ข้อ: reproduce → trace → falsify → cross-reference</td><td><code>/debug-mantra</code>, แจ้ง bug, บอกว่าอะไรพัง/error, ส่ง stack trace หรือ log</td></tr>
    <tr><td>tdd</td><td>test-first แบบ red-green-refactor</td><td><code>/tdd</code>, พูดถึง TDD, &quot;red-green-refactor&quot;, ให้เขียน test ก่อน</td></tr>
    <tr><td>codebase-design</td><td>คำศัพท์และหลักออกแบบ deep module: module, interface, seam, adapter (tdd เรียกใช้ตอนต้องเลือกว่าจะวาง seam ตรงไหน)</td><td><code>/codebase-design</code>, ออกแบบหรือปรับ interface ของ module, หาจุดวาง seam, ทำให้โค้ด test ง่ายขึ้น</td></tr>
    <tr><td>verification-before-completion</td><td>บังคับให้รันคำสั่งตรวจและดูผลก่อนบอกว่าเสร็จ แก้แล้ว หรือผ่าน</td><td><code>/verification-before-completion</code>, ก่อนบอกว่างานเสร็จ ก่อน commit หรือเปิด PR</td></tr>
    <tr><td>playwright-cli</td><td>ควบคุม browser, ทดสอบหน้าเว็บ, ตรวจ selector และถ่าย screenshot ผ่าน CLI</td><td><code>/playwright-cli</code>, ทดสอบ flow บนเว็บ, ตรวจหน้าเว็บใน browser, ขอ screenshot</td></tr>
    <tr><td>reverse-engineer-anything</td><td>วิเคราะห์ย้อนกลับแอป, binary และพฤติกรรม runtime ผ่าน REA (ต้องติดตั้ง REA MCP ก่อน)</td><td><code>/reverse-engineer-anything</code>, ขอ reverse engineer หรือ decompile แอปที่ build แล้ว (ไม่ใช่ source ใน repo)</td></tr>
    <tr><th colspan="3" align="left">ค้นหาเอกสาร</th></tr>
    <tr><td>find-docs</td><td>ดึงเอกสารล่าสุดของ library/CLI/cloud service ผ่าน <code>npx ctx7</code></td><td><code>/find-docs</code>, ถามเรื่อง API, config, migration ของ library ที่ระบุชื่อ</td></tr>
    <tr><th colspan="3" align="left">จัดการและสร้าง skill</th></tr>
    <tr><td>find-skills</td><td>ค้นหาและติดตั้ง skill</td><td><code>/find-skills</code>, &quot;find a skill for X&quot;, &quot;is there a skill that...&quot;</td></tr>
    <tr><td>skill-creator</td><td>สร้าง/แก้/วัดผล skill</td><td><code>/skill-creator</code>, อยากสร้างหรือปรับ skill, รัน eval ของ skill</td></tr>
  </tbody>
</table>

### ไฟล์และโฟลเดอร์ที่ skill อาจสร้าง

<table>
  <thead>
    <tr><th>Skill</th><th>ไฟล์/โฟลเดอร์</th><th>เกิดเมื่อ</th></tr>
  </thead>
  <tbody>
    <tr><td>design-taste-frontend</td><td><code>.taste-skill/</code>, <code>assets/</code> (คัดลอกจาก skill รวม <code>assets/img/credits.json</code> และ <code>assets/icons/icons-credits.json</code>), <code>shots/</code>, <code>names.json</code></td><td>สร้างหน้าเว็บ ดึงรูปหรือ icon และตรวจหน้าเว็บ</td></tr>
    <tr><td>playwright-cli</td><td><code>.playwright-cli/</code>, screenshot, trace, video</td><td>ใช้ browser CLI แม้เปิดเว็บ UAT</td></tr>
    <tr><td>setup-matt-pocock-skills</td><td><code>docs/agents/issue-tracker.md</code>, <code>docs/agents/domain.md</code></td><td>ตั้งค่า repo ครั้งแรก</td></tr>
    <tr><td>story</td><td><code>.story/&lt;issue&gt;-&lt;slug&gt;/</code> (spec, progress, screenshot, evidence และ prompt, คำตอบ, log ของ CLI เมื่อใช้ <code>cli</code>), บรรทัด <code>.story/</code> และ output ของ Playwright ใน <code>.git/info/exclude</code></td><td>เริ่ม <code>/story</code> ใน repo</td></tr>
    <tr><td>to-spec, to-tickets</td><td><code>.scratch/&lt;feature&gt;/</code></td><td>เลือก issue tracker แบบไฟล์ local (ถ้าเลือก GitHub/GitLab จะสร้างเป็น issue แทน)</td></tr>
    <tr><td>impeccable</td><td><code>.impeccable/</code>, <code>PRODUCT.md</code>, <code>DESIGN.md</code>, hook config</td><td>ใช้ workflow ออกแบบ, live หรือเปิด hooks</td></tr>
    <tr><td>skill-creator</td><td><code>&lt;skill-name&gt;-workspace/</code>, <code>evals/</code>, <code>*.skill</code></td><td>สร้าง skill, รัน eval หรือ package</td></tr>
    <tr><td>reverse-engineer-anything</td><td>recovered source, analysis cache, evidence JSON</td><td>recover/export ตามปลายทางที่เลือก</td></tr>
    <tr><td>find-skills</td><td>โฟลเดอร์ skill และไฟล์ติดตั้งของ agent</td><td>ติดตั้งหรือสร้าง skill แบบ project scope</td></tr>
  </tbody>
</table>

## MCP

ตรวจด้วย `claude mcp list` และ `codex mcp list` (config อยู่ที่ `~/.claude.json` และ `~/.codex/config.toml`) ไม่นับ connector จาก claude.ai เช่น Claude Docs เพราะไม่ได้ลงในเครื่อง

<table>
  <thead>
    <tr><th>MCP</th><th>Claude</th><th>Codex</th><th>ใช้กับ skill</th><th>คำสั่งติดตั้ง</th></tr>
  </thead>
  <tbody>
    <tr><td>REA</td><td>✅</td><td>✅ (ปิดใช้งาน)</td><td>reverse-engineer-anything</td><td><code>npx -y rea-agents@latest setup --client claude_code --client codex --skill=false</code> (ใช้กับเว็บ/JS ไม่ต้องลง engine เพิ่ม, <code>--skill=false</code> เพราะ skill มาจาก <code>npx skills</code> อยู่แล้ว)</td></tr>
    <tr><td>Context7</td><td>❌</td><td>❌</td><td>—</td><td>ไม่ลง: find-docs ใช้ <code>npx ctx7</code> ได้โดยไม่ต้องมี MCP</td></tr>
  </tbody>
</table>

### เปิด/ปิด REA ใน Codex

ติดตั้งไว้แต่ปิดเป็นค่าเริ่มต้นด้วย `enabled = false` ใน section `[mcp_servers.rea]` ของ `~/.codex/config.toml` โดยเก็บค่า `command`, `args` และค่าอื่นเดิมไว้

- เมื่อต้องใช้ `reverse-engineer-anything`: เปลี่ยนเป็น `enabled = true` แล้ว restart แอป/extension ที่ใช้งาน หรือเปิด Codex CLI session ใหม่
- เมื่อใช้เสร็จ: เปลี่ยนกลับเป็น `enabled = false` แล้วโหลด config ใหม่ด้วยวิธีเดียวกัน
- Skill ไม่ได้เปิด MCP ที่ถูกปิดให้อัตโนมัติ ต้องเปิดก่อนเรียก tools ของ REA
- Context7 MCP ไม่ได้ติดตั้ง: `find-docs` ใช้ `npx ctx7` ได้โดยไม่ต้องเปิด MCP

อ้างอิง: [OpenAI MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

## จัดการ skill

ติดตั้งและดูแล skill ด้วย [`npx skills`](https://github.com/vercel-labs/skills)
