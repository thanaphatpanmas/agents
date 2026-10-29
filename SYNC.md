# Agent Setup

> **Last updated:** 2026-10-28 Asia/Bangkok (UTC+07:00)

`~/.agents` คือที่เก็บหลัก (`npx skills` ลง skill ที่นี่) Claude ใช้ symlink ใน `~/.claude/skills` ส่วนคอลัมน์ Codex ตรวจเฉพาะ `~/.codex/skills`: ❌ = ไม่มีไฟล์/symlink (ที่ถูกต้อง), ✅ = มี symlink หลุดเข้ามา ทั้งที่ Codex เห็น skill ผ่าน `~/.agents/skills` เองอยู่แล้ว

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

### Sync

<table>
  <thead>
    <tr><th>Skill</th><th>Agents</th><th>Claude</th><th>Codex</th><th>ลิงก์ติดตั้ง</th></tr>
  </thead>
  <tbody>
    <tr><th colspan="5" align="left">วางแผนและจัดการงาน</th></tr>
    <tr><td>brainstorming</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/obra/superpowers/tree/main/skills/brainstorming">brainstorming</a></td></tr>
    <tr><td>commit</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thanaphatpanmas/agents/tree/main/skills/commit">commit</a></td></tr>
    <tr><td>workload</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thanaphatpanmas/agents/tree/main/skills/workload">workload</a></td></tr>
    <tr><td>short-notes</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thanaphatpanmas/agents/tree/main/skills/short-notes">short-notes</a></td></tr>
    <tr><td>caveman</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/juliusbrussee/caveman/caveman">caveman</a></td></tr>
    <tr><th colspan="5" align="left">ออกแบบและพัฒนา Frontend</th></tr>
    <tr><td>design-taste-frontend</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/Leonxlnx/taste-skill">taste-skill</a></td></tr>
    <tr><td>impeccable</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/pbakaus/impeccable">impeccable</a></td></tr>
    <tr><td>modern-web-guidance</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/googlechrome/modern-web-guidance/modern-web-guidance">modern-web-guidance</a></td></tr>
    <tr><td>typescript-magician</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mcollina/skills/typescript-magician">typescript-magician</a></td></tr>
    <tr><td>vercel-react-best-practices</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices">vercel-react-best-practices</a></td></tr>
    <tr><td>vercel-composition-patterns</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/vercel-labs/agent-skills/vercel-composition-patterns">vercel-composition-patterns</a></td></tr>
    <tr><th colspan="5" align="left">ฐานข้อมูล</th></tr>
    <tr><td>supabase-postgres-best-practices</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices">supabase-postgres-best-practices</a></td></tr>
    <tr><th colspan="5" align="left">คุณภาพ ประสิทธิภาพ และ SEO</th></tr>
    <tr><td>best-practices</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://officialskills.sh/addyosmani/skills/best-practices">best-practices</a></td></tr>
    <tr><td>performance</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://officialskills.sh/addyosmani/skills/performance">performance</a></td></tr>
    <tr><td>seo</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://officialskills.sh/addyosmani/skills/seo">seo</a></td></tr>
    <tr><th colspan="5" align="left">Debug ทดสอบ และวิเคราะห์ระบบ</th></tr>
    <tr><td>debug-mantra</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/thananon/9arm-skills/blob/main/skills/engineering/debug-mantra/SKILL.md">debug-mantra</a></td></tr>
    <tr><td>tdd</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/mattpocock/skills/tdd">tdd</a></td></tr>
    <tr><td>playwright-cli</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/microsoft/playwright-cli/tree/main/skills/playwright-cli">playwright-cli</a></td></tr>
    <tr><td>reverse-engineer-anything</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://github.com/morluto/rea">REA</a></td></tr>
    <tr><th colspan="5" align="left">ค้นหาเอกสาร</th></tr>
    <tr><td>find-docs</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/upstash/context7/find-docs">find-docs</a></td></tr>
    <tr><td>context7-cli</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/upstash/context7/context7-cli">context7-cli</a></td></tr>
    <tr><td>context7-mcp</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/upstash/context7/context7-mcp">context7-mcp</a></td></tr>
    <tr><th colspan="5" align="left">จัดการและสร้าง skill</th></tr>
    <tr><td>find-skills</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/vercel-labs/skills/find-skills">find-skills</a></td></tr>
    <tr><td>skill-creator</td><td>✅</td><td>✅ (symlink)</td><td>❌</td><td><a href="https://skills.sh/anthropics/skills/skill-creator">skill-creator</a></td></tr>
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
    <tr><td>brainstorming</td><td>ช่วยระดมความคิด คุย requirement และออกแบบแนวทางก่อนเริ่มสร้างหรือเปลี่ยนพฤติกรรม</td><td><code>/brainstorming</code>, ขอระดมความคิดหรือออกแบบแนวทางก่อนลงมือ</td></tr>
    <tr><td>commit</td><td>stage ทุกไฟล์ใน repo ปัจจุบันหรือโปรเจกต์ที่ระบุ commit แบบ Conventional Commits จาก diff แล้วให้เลือก commit อย่างเดียวหรือ commit + push</td><td><code>/commit</code>, &quot;commit and push&quot;, สั่ง commit/push เป็นภาษาไหนก็ได้</td></tr>
    <tr><td>workload</td><td>สรุป git commit ตามช่วงวันที่เป็น workload รายสัปดาห์ เติมให้ครบวันละ 8 ชม.</td><td><code>/workload</code>, ลงเวลา/ลงงาน/สรุปงานประจำสัปดาห์, ส่ง week ที่มีช่อง <code>[]</code> ว่าง</td></tr>
    <tr><td>short-notes</td><td>เขียน/แก้โน้ตส่วนตัว Markdown สไตล์ bullet + code เลือกภาษาไทย/อังกฤษ และระดับ brief/medium/detailed</td><td><code>/short-notes</code>, ขอจด/บันทึก/สรุปลงโน้ต, เพิ่มหรือเขียนโน้ต .md เดิมใหม่</td></tr>
    <tr><td>caveman</td><td>ตอบสั้นแบบ caveman ลด token เปิดค้างทั้ง session จนพูด &quot;stop caveman&quot; หรือ &quot;normal mode&quot;</td><td><code>/caveman</code>, &quot;caveman mode&quot;, &quot;be brief&quot;, &quot;less tokens&quot;</td></tr>
    <tr><th colspan="3" align="left">ออกแบบและพัฒนา Frontend</th></tr>
    <tr><td>design-taste-frontend</td><td>ออกแบบเว็บ/หน้าแอปไม่ให้ดู generic: เลือก art direction แล้วตรวจผลใน browser จริง</td><td><code>/design-taste-frontend</code>, สร้าง/รีดีไซน์เว็บ, landing page, dashboard, บอกว่าหน้าดู generic/&quot;AI-made&quot;</td></tr>
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
    <tr><td>playwright-cli</td><td>ควบคุม browser, ทดสอบหน้าเว็บ, ตรวจ selector และถ่าย screenshot ผ่าน CLI</td><td><code>/playwright-cli</code>, ทดสอบ flow บนเว็บ, ตรวจหน้าเว็บใน browser, ขอ screenshot</td></tr>
    <tr><td>reverse-engineer-anything</td><td>วิเคราะห์ย้อนกลับแอป, binary และพฤติกรรม runtime ผ่าน REA (ต้องติดตั้ง REA MCP ก่อน)</td><td><code>/reverse-engineer-anything</code>, ขอ reverse engineer หรือ decompile แอปที่ build แล้ว (ไม่ใช่ source ใน repo)</td></tr>
    <tr><th colspan="3" align="left">ค้นหาเอกสาร</th></tr>
    <tr><td>find-docs</td><td>ดึงเอกสารล่าสุดของ library/CLI/cloud service ผ่าน <code>npx ctx7</code></td><td><code>/find-docs</code>, ถามเรื่อง API, config, migration ของ library ที่ระบุชื่อ</td></tr>
    <tr><td>context7-cli</td><td>ใช้ CLI <code>ctx7</code> (ผ่าน <code>npx</code>) ดึงเอกสาร library และตั้งค่า Context7 MCP</td><td><code>/context7-cli</code>, พูดถึง &quot;ctx7&quot; หรือ &quot;context7&quot;, ตั้งค่า Context7</td></tr>
    <tr><td>context7-mcp</td><td>ดึงเอกสาร/ตัวอย่างโค้ด library ผ่าน Context7 MCP (ต้องติดตั้ง MCP ก่อน)</td><td><code>/context7-mcp</code>, ถามเรื่อง library/framework, ขอตัวอย่างโค้ด</td></tr>
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
    <tr><td>design-taste-frontend</td><td><code>.taste-skill/</code>, <code>assets/credits.json</code></td><td>เลือก direction, ตรวจหน้าเว็บ หรือดาวน์โหลด assets</td></tr>
    <tr><td>playwright-cli</td><td><code>.playwright-cli/</code>, screenshot, trace, video</td><td>ใช้ browser CLI แม้เปิดเว็บ UAT</td></tr>
    <tr><td>brainstorming</td><td><code>.superpowers/brainstorm/</code>, <code>docs/superpowers/specs/</code></td><td>ใช้ visual companion แบบเก็บในโปรเจกต์ หรือเขียน design spec</td></tr>
    <tr><td>impeccable</td><td><code>.impeccable/</code>, <code>PRODUCT.md</code>, <code>DESIGN.md</code>, hook config</td><td>ใช้ workflow ออกแบบ, live หรือเปิด hooks</td></tr>
    <tr><td>skill-creator</td><td><code>&lt;skill-name&gt;-workspace/</code>, <code>evals/</code>, <code>*.skill</code></td><td>สร้าง skill, รัน eval หรือ package</td></tr>
    <tr><td>reverse-engineer-anything</td><td>recovered source, analysis cache, evidence JSON</td><td>recover/export ตามปลายทางที่เลือก</td></tr>
    <tr><td>context7-cli</td><td><code>.mcp.json</code> หรือ config/rules/skills ของ agent</td><td>ใช้ <code>setup --project</code></td></tr>
    <tr><td>find-skills</td><td>โฟลเดอร์ skill และไฟล์ติดตั้งของ agent</td><td>ติดตั้งหรือสร้าง skill แบบ project scope</td></tr>
  </tbody>
</table>

## จัดการ skill

ติดตั้งและดูแล skill ด้วย [`npx skills`](https://github.com/vercel-labs/skills)
