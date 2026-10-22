# Agent Setup

> **Last updated:** 2026-10-22 13:12:00 Asia/Bangkok (UTC+07:00)

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

| Skill                            | ทำอะไร                                                                      | ทำงานเมื่อ                                | Agents | Claude       | Codex | ลิงก์ติดตั้ง                                                                                                 |
| -------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------- | ------ | ------------ | ----- | ------------------------------------------------------------------------------------------------------------ |
| best-practices                   | ตรวจ/ปรับโค้ดเว็บตาม best practice ด้าน security, compatibility, คุณภาพโค้ด | พูดว่า "security audit", "modernize code" | ✅     | ✅ (symlink) | ❌    | [best-practices](https://officialskills.sh/addyosmani/skills/best-practices)                                 |
| performance                      | เพิ่มความเร็วเว็บ ลดเวลาโหลด                                                | พูดว่า "speed up", "performance audit"    | ✅     | ✅ (symlink) | ❌    | [performance](https://officialskills.sh/addyosmani/skills/performance)                                       |
| seo                              | ปรับ meta tag, structured data, sitemap                                     | พูดว่า "improve SEO"                      | ✅     | ✅ (symlink) | ❌    | [seo](https://officialskills.sh/addyosmani/skills/seo)                                                       |
| caveman                          | ตอบสั้นแบบ caveman ลด token (ระดับ lite/full/ultra)                         | `/caveman`, "be brief", "less tokens"     | ✅     | ✅ (symlink) | ❌    | [caveman](https://skills.sh/juliusbrussee/caveman/caveman)                                                   |
| debug-mantra                     | วินัย debug 4 ข้อ: reproduce → trace → falsify → cross-reference            | เริ่ม debug, ส่ง stack trace              | ✅     | ✅ (symlink) | ❌    | [debug-mantra](https://github.com/thananon/9arm-skills/blob/main/skills/engineering/debug-mantra/SKILL.md)   |
| context7-cli                     | ใช้ CLI `ctx7` ดึงเอกสาร library และจัดการ skill                            | พูดถึง "ctx7", "context7"                 | ✅     | ✅ (symlink) | ❌    | [context7-cli](https://skills.sh/upstash/context7/context7-cli)                                              |
| context7-mcp                     | ดึงเอกสาร/ตัวอย่างโค้ด library ผ่าน MCP                                     | ถามเรื่อง library, framework              | ✅     | ✅ (symlink) | ❌    | [context7-mcp](https://skills.sh/upstash/context7/context7-mcp)                                              |
| find-docs                        | ดึงเอกสารล่าสุดของ library/CLI/cloud service                                | ถามเรื่อง API, config, migration          | ✅     | ✅ (symlink) | ❌    | [find-docs](https://skills.sh/upstash/context7/find-docs)                                                    |
| find-skills                      | ค้นหาและติดตั้ง skill                                                       | "find a skill for X"                      | ✅     | ✅ (symlink) | ❌    | [find-skills](https://skills.sh/vercel-labs/skills/find-skills)                                              |
| skill-creator                    | สร้าง/แก้/วัดผล skill                                                       | อยากสร้างหรือปรับ skill                   | ✅     | ✅ (symlink) | ❌    | [skill-creator](https://skills.sh/anthropics/skills/skill-creator)                                           |
| modern-web-guidance              | คำแนะนำ HTML/CSS/JS ฝั่ง client แบบใหม่ จาก Google Chrome                   | งาน UI, layout, scroll, web API           | ✅     | ✅ (symlink) | ❌    | [modern-web-guidance](https://skills.sh/googlechrome/modern-web-guidance/modern-web-guidance)                |
| typescript-magician              | generic type, ลบ `any`, type guard, แก้ compiler error                      | ถามเรื่อง type                            | ✅     | ✅ (symlink) | ❌    | [typescript-magician](https://skills.sh/mcollina/skills/typescript-magician)                                 |
| supabase-postgres-best-practices | schema, migration, RLS, index, query ช้า                                    | งาน Postgres                              | ✅     | ✅ (symlink) | ❌    | [supabase-postgres-best-practices](https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices) |
| vercel-react-best-practices      | ปรับ performance ของ React/Next.js                                          | เขียน/รีวิว React                         | ✅     | ✅ (symlink) | ❌    | [vercel-react-best-practices](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices)        |
| vercel-composition-patterns      | compound component, render props, context                                   | ออกแบบ component                          | ✅     | ✅ (symlink) | ❌    | [vercel-composition-patterns](https://skills.sh/vercel-labs/agent-skills/vercel-composition-patterns)        |
| tdd                              | test-first แบบ red-green-refactor                                           | พูดถึง TDD, ให้ทำ test ก่อน               | ✅     | ✅ (symlink) | ❌    | [tdd](https://skills.sh/mattpocock/skills/tdd)                                                               |
| reverse-engineer-anything        | วิเคราะห์ย้อนกลับแอป, binary และพฤติกรรม runtime ผ่าน REA                  | ขอ reverse engineer หรือแกะการทำงานแอป   | ✅     | ✅ (symlink) | ❌    | [REA](https://github.com/morluto/rea)                                                                       |
| short-notes                      | เขียน/แก้โน้ตส่วนตัวแบบ Markdown (cheat sheet, setup, how-to) ในสไตล์ bullet + code สั้น กระชับ | ขอจด/สรุป/เพิ่ม/เขียนโน้ตใหม่            | ✅     | ✅ (symlink) | ❌    | [short-notes](https://github.com/thanaphatpanmas/agents/tree/main/skills/short-notes)                        |
| commit                           | stage ทุกไฟล์ commit แบบ Conventional Commits จาก diff แล้วถามว่า push ไหม  | `/commit`, "commit and push"              | ✅     | ✅ (symlink) | ❌    | [commit](https://github.com/thanaphatpanmas/agents/tree/main/skills/commit)                                  |
| workload                         | สรุป git commit ตามช่วงวันที่เป็น workload รายสัปดาห์ เติมให้ครบวันละ 8 ชม. | `/workload`, ลงเวลา/ลงงาน/สรุปงานสัปดาห์  | ✅     | ✅ (symlink) | ❌    | [workload](https://github.com/thanaphatpanmas/agents/tree/main/skills/workload)                              |

## จัดการ skill

ติดตั้งและดูแล skill ด้วย [`npx skills`](https://github.com/vercel-labs/skills)
