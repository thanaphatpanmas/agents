# Agent Setup

> **Last updated:** 2026-10-23 14:56:53 Asia/Bangkok (UTC+07:00)

`~/.agents` คือที่เก็บหลัก (`npx skills` ลง skill ที่นี่) Claude ใช้ symlink ใน `~/.claude/skills` ส่วนคอลัมน์ Codex ตรวจเฉพาะ `~/.codex/skills`: ❌ = ไม่มีไฟล์/symlink (ที่ถูกต้อง), ✅ = มี symlink หลุดเข้ามา ทั้งที่ Codex เห็น skill ผ่าน `~/.agents/skills` เองอยู่แล้ว

## Instruction file

แยก 2 ระดับ: Global ใช้กับทุกโปรเจกต์, Project อยู่ใน repo และใช้เฉพาะโปรเจกต์นั้น

### Global

|        | ไฟล์                  | ชนิด                                  |
| ------ | --------------------- | ------------------------------------- |
| Repo   | `~/Development/Projects/agents/AGENTS.md` | ไฟล์จริง (ต้นฉบับ)            |
| Agents | `~/.agents/AGENTS.md` | symlink → ต้นฉบับใน repo              |
| Claude | `~/.claude/CLAUDE.md` | symlink → ต้นฉบับใน repo              |
| Codex  | `~/.codex/AGENTS.md`  | symlink → ต้นฉบับใน repo              |

แก้ที่ `AGENTS.md` ใน repo ไฟล์เดียว ทั้งสามที่จะเปลี่ยนตามอัตโนมัติ

### Project

| ไฟล์                        | ทำอะไร                                                                                  |
| --------------------------- | --------------------------------------------------------------------------------------- |
| `AGENTS.md`                 | กฎการทำงานของ agent: อ่านอะไรก่อนแก้, ใช้ skill ไหน, คำสั่ง verify, วิธีอัปเดตเอกสาร    |
| `CLAUDE.md`                 | มีแค่ `@AGENTS.md` เพื่อให้ Claude Code อ่านไฟล์เดียวกับ agent อื่น                     |
| `ARCHITECTURE.md`           | โครงสร้าง package/module, ที่วางไฟล์, data flow, i18n ownership, API naming, มาตรฐาน UI |
| `DESIGN.md`                 | token และสเปกภาพของดีไซน์ (ส่วนบน = ของที่ import มา, ส่วนล่าง = override ของโปรเจกต์)  |
| `docs/*.md`                 | เอกสารเฉพาะเรื่อง เช่น `overview.md`, `date-time.md`, `tech-stack.md` อ่านเมื่อแตะงานนั้น              |
| `.agents/skills/*/SKILL.md` | ขั้นตอนเฉพาะงาน เช่น สร้าง module, reports, permissions                                 |

## Skills (`~/.agents/skills`)

### Sync

| Skill                            | Agents | Claude       | Codex | ลิงก์ติดตั้ง                                                                                                      |
| -------------------------------- | ------ | ------------ | ----- | ------------------------------------------------------------------------------------------------------------ |
| best-practices                   | ✅     | ✅ (symlink) | ❌    | [best-practices](https://officialskills.sh/addyosmani/skills/best-practices)                                 |
| performance                      | ✅     | ✅ (symlink) | ❌    | [performance](https://officialskills.sh/addyosmani/skills/performance)                                       |
| seo                              | ✅     | ✅ (symlink) | ❌    | [seo](https://officialskills.sh/addyosmani/skills/seo)                                                       |
| caveman                          | ✅     | ✅ (symlink) | ❌    | [caveman](https://skills.sh/juliusbrussee/caveman/caveman)                                                   |
| debug-mantra                     | ✅     | ✅ (symlink) | ❌    | [debug-mantra](https://github.com/thananon/9arm-skills/blob/main/skills/engineering/debug-mantra/SKILL.md)   |
| context7-cli                     | ✅     | ✅ (symlink) | ❌    | [context7-cli](https://skills.sh/upstash/context7/context7-cli)                                              |
| context7-mcp                     | ✅     | ✅ (symlink) | ❌    | [context7-mcp](https://skills.sh/upstash/context7/context7-mcp)                                              |
| find-docs                        | ✅     | ✅ (symlink) | ❌    | [find-docs](https://skills.sh/upstash/context7/find-docs)                                                    |
| find-skills                      | ✅     | ✅ (symlink) | ❌    | [find-skills](https://skills.sh/vercel-labs/skills/find-skills)                                              |
| skill-creator                    | ✅     | ✅ (symlink) | ❌    | [skill-creator](https://skills.sh/anthropics/skills/skill-creator)                                           |
| modern-web-guidance              | ✅     | ✅ (symlink) | ❌    | [modern-web-guidance](https://skills.sh/googlechrome/modern-web-guidance/modern-web-guidance)                |
| typescript-magician              | ✅     | ✅ (symlink) | ❌    | [typescript-magician](https://skills.sh/mcollina/skills/typescript-magician)                                 |
| supabase-postgres-best-practices | ✅     | ✅ (symlink) | ❌    | [supabase-postgres-best-practices](https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices) |
| vercel-react-best-practices      | ✅     | ✅ (symlink) | ❌    | [vercel-react-best-practices](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices)        |
| vercel-composition-patterns      | ✅     | ✅ (symlink) | ❌    | [vercel-composition-patterns](https://skills.sh/vercel-labs/agent-skills/vercel-composition-patterns)        |
| tdd                              | ✅     | ✅ (symlink) | ❌    | [tdd](https://skills.sh/mattpocock/skills/tdd)                                                               |
| design-taste-frontend            | ✅     | ✅ (symlink) | ❌    | [taste-skill](https://github.com/Leonxlnx/taste-skill)                                                       |
| reverse-engineer-anything        | ✅     | ✅ (symlink) | ❌    | [REA](https://github.com/morluto/rea)                                                                        |
| short-notes                      | ✅     | ✅ (symlink) | ❌    | [short-notes](https://github.com/thanaphatpanmas/agents/tree/main/skills/short-notes)                        |
| commit                           | ✅     | ✅ (symlink) | ❌    | [commit](https://github.com/thanaphatpanmas/agents/tree/main/skills/commit)                                  |
| workload                         | ✅     | ✅ (symlink) | ❌    | [workload](https://github.com/thanaphatpanmas/agents/tree/main/skills/workload)                              |

### การใช้งาน

พิมพ์ `/ชื่อ-skill` เพื่อเรียกได้แน่นอน คำอื่นในคอลัมน์ "ทำงานเมื่อ" แค่ช่วยให้ agent เลือก skill นั้นเอง (ดูจาก description ไม่ใช่จับ keyword ตรงตัว)

| Skill                            | ทำอะไร                                                                                                                     | ทำงานเมื่อ                                                                                             |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| best-practices                   | ตรวจ/ปรับโค้ดเว็บตาม best practice ด้าน security, compatibility, คุณภาพโค้ด                                                      | `/best-practices`, "security audit", "modernize code", "check for vulnerabilities"                   |
| performance                      | เพิ่มความเร็วเว็บ ลดเวลาโหลด                                                                                                   | `/performance`, "speed up my site", "performance audit", เว็บโหลดช้า                                   |
| seo                              | ปรับ meta tag, structured data, sitemap                                                                                     | `/seo`, "improve SEO", "fix meta tags"                                                               |
| caveman                          | ตอบสั้นแบบ caveman ลด token เปิดค้างทั้ง session จนพูด "stop caveman" หรือ "normal mode"                                           | `/caveman`, "caveman mode", "be brief", "less tokens"                                                |
| debug-mantra                     | วินัย debug 4 ข้อ: reproduce → trace → falsify → cross-reference                                                              | `/debug-mantra`, แจ้ง bug, บอกว่าอะไรพัง/error, ส่ง stack trace หรือ log                                  |
| context7-cli                     | ใช้ CLI `ctx7` (ผ่าน `npx`) ดึงเอกสาร library และตั้งค่า Context7 MCP                                                            | `/context7-cli`, พูดถึง "ctx7" หรือ "context7", ตั้งค่า Context7                                           |
| context7-mcp                     | ดึงเอกสาร/ตัวอย่างโค้ด library ผ่าน Context7 MCP (ต้องติดตั้ง MCP ก่อน)                                                              | `/context7-mcp`, ถามเรื่อง library/framework, ขอตัวอย่างโค้ด                                              |
| find-docs                        | ดึงเอกสารล่าสุดของ library/CLI/cloud service ผ่าน `npx ctx7`                                                                   | `/find-docs`, ถามเรื่อง API, config, migration ของ library ที่ระบุชื่อ                                      |
| find-skills                      | ค้นหาและติดตั้ง skill                                                                                                          | `/find-skills`, "find a skill for X", "is there a skill that..."                                     |
| skill-creator                    | สร้าง/แก้/วัดผล skill                                                                                                         | `/skill-creator`, อยากสร้างหรือปรับ skill, รัน eval ของ skill                                            |
| modern-web-guidance              | แนวทาง HTML/CSS/JS ฝั่ง client แบบใหม่ จาก Google Chrome                                                                      | `/modern-web-guidance`, งาน UI, layout, scroll/animation, web API, ฟอร์ม, accessibility               |
| typescript-magician              | generic type, ลบ `any`, type guard, แก้ compiler error                                                                      | `/typescript-magician`, ถามเรื่อง TypeScript type, generic, ลบ `any`, type error                       |
| supabase-postgres-best-practices | ออกแบบ schema, migration, RLS, index, แก้ query ช้า                                                                          | `/supabase-postgres-best-practices`, งาน Postgres ทุกอย่าง แม้แก้คอลัมน์เดียว                               |
| vercel-react-best-practices      | ปรับ performance ของ React/Next.js                                                                                          | `/vercel-react-best-practices`, เขียน/รีวิว/refactor React หรือ Next.js                                  |
| vercel-composition-patterns      | แก้ component ที่มี boolean prop เยอะ ด้วย compound component, render props, context                                            | `/vercel-composition-patterns`, props เยอะเกิน, ทำ component library, วางโครง component               |
| tdd                              | test-first แบบ red-green-refactor                                                                                          | `/tdd`, พูดถึง TDD, "red-green-refactor", ให้เขียน test ก่อน                                              |
| design-taste-frontend            | ออกแบบเว็บ/หน้าแอปไม่ให้ดู generic: เลือก art direction แล้วตรวจผลใน browser จริง                                                  | `/design-taste-frontend`, สร้าง/รีดีไซน์เว็บ, landing page, dashboard, บอกว่าหน้าดู generic/"AI-made"        |
| reverse-engineer-anything        | วิเคราะห์ย้อนกลับแอป, binary และพฤติกรรม runtime ผ่าน REA (ต้องติดตั้ง REA MCP ก่อน)                                                  | `/reverse-engineer-anything`, ขอ reverse engineer หรือ decompile แอปที่ build แล้ว (ไม่ใช่ source ใน repo) |
| short-notes                      | เขียน/แก้โน้ตส่วนตัว Markdown สไตล์ bullet + code เลือกภาษาไทย/อังกฤษ และระดับ brief/medium/detailed                                | `/short-notes`, ขอจด/บันทึก/สรุปลงโน้ต, เพิ่มหรือเขียนโน้ต .md เดิมใหม่                                         |
| commit                           | stage ทุกไฟล์ใน repo ปัจจุบันหรือโปรเจกต์ที่ระบุ commit แบบ Conventional Commits จาก diff แล้วให้เลือก commit อย่างเดียวหรือ commit + push | `/commit`, "commit and push", สั่ง commit/push เป็นภาษาไหนก็ได้                                           |
| workload                         | สรุป git commit ตามช่วงวันที่เป็น workload รายสัปดาห์ เติมให้ครบวันละ 8 ชม.                                                           | `/workload`, ลงเวลา/ลงงาน/สรุปงานประจำสัปดาห์, ส่ง week ที่มีช่อง `[]` ว่าง                                   |

## จัดการ skill

ติดตั้งและดูแล skill ด้วย [`npx skills`](https://github.com/vercel-labs/skills)
