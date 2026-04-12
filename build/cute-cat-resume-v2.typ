// ============================================================
// 🐱 可爱小猫简历 — Cute Cat Resume v2
// 基于 Typst Skill 参考文档指导编写
// ============================================================

// --- 全局设置 ---
// 参考: chinese-typesetting.md — 字体回退链 + 语言设置
#set page(
  paper: "a4",
  margin: (top: 1.2cm, bottom: 1.2cm, left: 1.2cm, right: 1.2cm),
  fill: rgb("#FFF8F0"),  // 暖色调米白背景
)
#set text(
  font: (
    "Source Han Sans SC",
    "Noto Sans CJK SC",
    "Microsoft YaHei",
    "PingFang SC",
    "SimHei",
  ),
  size: 10pt,
  lang: "zh",
  region: "cn",
)
#set par(leading: 0.7em)

// --- 颜色定义 ---
// 参考: visualize.md — rgb() 颜色创建
#let pink-primary = rgb("#FF6B9D")
#let pink-light = rgb("#FFE0EB")
#let pink-dark = rgb("#D4457A")
#let warm-bg = rgb("#FFF0F5")
#let cream = rgb("#FFFAF0")
#let coral = rgb("#FF7F7F")
#let lavender = rgb("#E8D5F5")
#let mint = rgb("#D5F5E3")
#let peach = rgb("#FFDAB9")
#let gold = rgb("#FFD700")
#let text-dark = rgb("#4A3728")
#let text-gray = rgb("#8B7D6B")

// ============================================================
// 辅助函数
// 参考: scripting-and-context.md — let 函数定义
//       visualize.md — Card 组合模式 (rect + inset + radius + fill)
// ============================================================

// 节标题
#let section-title(icon, title) = {
  v(6pt)
  stack(dir: ltr, spacing: 6pt,
    text(size: 14pt)[#icon],
    text(size: 12pt, weight: "bold", fill: pink-dark)[#title],
  )
  v(2pt)
  line(length: 100%, stroke: 1.5pt + pink-light)
  v(4pt)
}

// 技能评级条
// 参考: scripting-and-context.md — for 循环 range()
//       visualize.md — rect 参数 (radius, fill)
#let skill-rating(name, level, max-level: 5) = {
  grid(
    columns: (1fr, auto),
    align: (left, right),
    text(size: 9pt, fill: text-dark)[#name],
    stack(dir: ltr, spacing: 2pt,
      ..range(max-level).map(i => {
        if i < level {
          circle(radius: 4pt, fill: pink-primary, stroke: none)
        } else {
          circle(radius: 4pt, fill: rgb("#F0E0E5"), stroke: 0.5pt + pink-light)
        }
      }),
    ),
  )
  v(3pt)
}

// 工作经历条目
// 参考: book-paper-slide-cv-patterns.md — cv-entry 模式
#let work-entry(title: "", period: "", company: "", details: ()) = {
  grid(
    columns: (auto, 1fr),
    gutter: 8pt,
    // 时间线圆点
    align(center)[
      #circle(radius: 4pt, fill: pink-primary, stroke: 0pt + white)
    ],
    // 内容
    {
      grid(
        columns: (1fr, auto),
        align: (left, right),
        text(size: 10pt, weight: "bold", fill: text-dark)[#title],
        text(size: 8pt, fill: text-gray)[#period],
      )
      text(size: 8pt, fill: pink-dark)[#company]
      v(2pt)
      for detail in details {
        text(size: 8.5pt, fill: text-dark)[- #detail]
        linebreak()
      }
      v(4pt)
    },
  )
}

// 标签徽章
// 参考: visualize.md — Badge 组合模式 (box + fill + radius + inset)
#let tag-badge(label, bg-color: pink-light) = {
  box(
    fill: bg-color,
    radius: 8pt,
    inset: (x: 7pt, y: 3pt),
    text(size: 8pt, fill: text-dark)[#label],
  )
}

// 信息行
#let info-row(icon, content-text) = {
  stack(dir: ltr, spacing: 4pt,
    text(size: 9pt)[#icon],
    text(size: 9pt, fill: text-dark)[#content-text],
  )
  v(2pt)
}

// ============================================================
// 简历正文
// ============================================================

// --- 头部横幅 ---
// 参考: visualize.md — gradient.linear(), rect with gradient fill
#block(
  width: 100%,
  inset: 0pt,
  radius: 12pt,
  clip: true,
)[
  #rect(
    width: 100%,
    height: 100pt,
    fill: gradient.linear(pink-primary, rgb("#FF9A76"), angle: 135deg),
    radius: 12pt,
  )[
    #align(center + horizon)[
      // 圆形头像占位
      // 参考: visualize.md — circle with fill and content
      #grid(
        columns: (auto, 1fr),
        gutter: 16pt,
        align: (center, left + horizon),
        circle(
          radius: 35pt,
          fill: white,
          stroke: 3pt + rgb("#FFFFFF80"),
        )[
          #align(center + horizon)[
            #text(size: 36pt)[🐱]
          ]
        ],
        {
          text(size: 22pt, weight: "bold", fill: white)[喵小萌]
          linebreak()
          v(4pt)
          text(size: 11pt, fill: rgb("#FFFFFFDD"))[
            #emoji.cat.face 资深捕鱼大师 | 首席卖萌官 (CMO)
          ]
        },
      )
    ]
  ]
]

v(8pt)

// --- 双栏主体 ---
// 参考: layout.md — grid(columns: (1fr, 2fr)) 双栏布局
#grid(
  columns: (1fr, 1.6fr),
  gutter: 12pt,

  // ============================================
  // 左栏 — 个人信息 + 技能 + 爱好
  // ============================================
  {
    // 个人信息卡片
    // 参考: visualize.md — rect with radius, fill, inset
    rect(
      width: 100%,
      fill: cream,
      stroke: 0.5pt + pink-light,
      radius: 10pt,
      inset: 12pt,
    )[
      #section-title(emoji.prints.paw, "个人信息")
      #info-row("📧", "miaoxm@catmail.com")
      #info-row("📱", "138-0000-MEOW")
      #info-row("🏠", "阳光花园小区 3 号猫窝")
      #info-row("🎂", "2022 年 6 月 1 日 (3 岁)")
      #info-row("🌐", "github.com/meow-coder")
    ]

    v(8pt)

    // 专业技能卡片
    rect(
      width: 100%,
      fill: cream,
      stroke: 0.5pt + pink-light,
      radius: 10pt,
      inset: 12pt,
    )[
      #section-title("⭐", "专业技能")
      #skill-rating("捕鱼技术", 5)
      #skill-rating("卖萌能力", 5)
      #skill-rating("跳跃身法", 4)
      #skill-rating("夜视侦察", 4)
      #skill-rating("团队协作", 3)
      #skill-rating("服从指挥", 2)
    ]

    v(8pt)

    // 语言能力卡片
    rect(
      width: 100%,
      fill: cream,
      stroke: 0.5pt + pink-light,
      radius: 10pt,
      inset: 12pt,
    )[
      #section-title("🗣", "语言能力")
      #skill-rating("喵喵语 (母语)", 5)
      #skill-rating("呼噜语", 4)
      #skill-rating("哈气语 (防御)", 3)
      #skill-rating("人类语 (听力)", 2)
    ]

    v(8pt)

    // 兴趣爱好卡片
    rect(
      width: 100%,
      fill: cream,
      stroke: 0.5pt + pink-light,
      radius: 10pt,
      inset: 12pt,
    )[
      #section-title("💕", "兴趣爱好")
      #grid(
        columns: (1fr, 1fr),
        gutter: 4pt,
        tag-badge("🐟 捕鱼", bg-color: mint),
        tag-badge("☀ 晒太阳", bg-color: peach),
        tag-badge("🧶 玩毛线", bg-color: lavender),
        tag-badge("📦 钻纸箱", bg-color: pink-light),
        tag-badge("🦎 追蜥蜴", bg-color: mint),
        tag-badge("😴 午睡", bg-color: peach),
      )
    ]
  },

  // ============================================
  // 右栏 — 个人简介 + 工作经历 + 荣誉 + 自我评价
  // ============================================
  {
    // 个人简介卡片
    rect(
      width: 100%,
      fill: cream,
      stroke: 0.5pt + pink-light,
      radius: 10pt,
      inset: 12pt,
    )[
      #section-title("💌", "个人简介")
      #text(size: 9pt, fill: text-dark)[
        本喵是一只拥有 3 年丰富捕鱼经验的资深猫咪，擅长各类高难度卖萌动作，
        熟练掌握「翻肚皮」「歪头杀」「慢眨眼」等核心技能。曾任多家人类家庭
        的首席治愈官，具备优秀的团队合作精神和独立自主的生活能力。
        希望在一个充满阳光和鱼罐头的环境中继续发挥所长！#emoji.sparkles
      ]
    ]

    v(8pt)

    // 工作经历卡片 — 时间线风格
    rect(
      width: 100%,
      fill: cream,
      stroke: 0.5pt + pink-light,
      radius: 10pt,
      inset: 12pt,
    )[
      #section-title("💼", "工作经历")
      #work-entry(
        title: "首席卖萌官 (CMO)",
        period: "2024.06 - 至今",
        company: "🏠 阳光花园张阿姨家",
        details: (
          "负责全家的心情管理，日均卖萌 30+ 次",
          "成功将家庭幸福指数提升 200%",
          "开发了「歪头杀」「慢眨眼」等独创卖萌技术",
        ),
      )
      #work-entry(
        title: "高级捕鱼工程师",
        period: "2023.08 - 2024.05",
        company: "🐟 小区锦鲤池塘",
        details: (
          "独立完成日均捕鱼目标 5 条",
          "优化了「闪电爪」捕鱼算法，效率提升 150%",
          "培训 2 名实习小猫掌握基础捕鱼技能",
        ),
      )
      #work-entry(
        title: "见习巡逻员",
        period: "2023.01 - 2023.07",
        company: "🏘 阳光花园物业",
        details: (
          "负责小区夜间安全巡逻",
          "成功驱逐入侵流浪狗 12 次",
        ),
      )
    ]

    v(8pt)

    // 荣誉证书卡片
    rect(
      width: 100%,
      fill: cream,
      stroke: 0.5pt + pink-light,
      radius: 10pt,
      inset: 12pt,
    )[
      #section-title("🏆", "荣誉证书")
      #grid(
        columns: (1fr, auto),
        row-gutter: 6pt,
        text(size: 9pt, fill: text-dark)[#emoji.trophy 年度最佳卖萌猫咪],
        text(size: 8pt, fill: text-gray)[2025],
        text(size: 9pt, fill: text-dark)[#emoji.medal.sports 小区捕鱼大赛冠军],
        text(size: 8pt, fill: text-gray)[2024],
        text(size: 9pt, fill: text-dark)[🎖 「最佳警觉奖」— 物业表彰],
        text(size: 8pt, fill: text-gray)[2023],
        text(size: 9pt, fill: text-dark)[💖 「最治愈猫咪」人气投票第一],
        text(size: 8pt, fill: text-gray)[2023],
      )
    ]

    v(8pt)

    // 自我评价卡片
    rect(
      width: 100%,
      fill: gradient.linear(rgb("#FFE0EB"), rgb("#FFF0F5"), angle: 135deg),
      stroke: 0.5pt + pink-light,
      radius: 10pt,
      inset: 12pt,
    )[
      #section-title("✨", "自我评价")
      #text(size: 9pt, fill: text-dark)[
        本喵性格温顺但不失活泼，工作态度认真负责（除了午睡时间）。
        拥有极强的适应能力，无论是沙发、纸箱还是键盘上都能迅速进入工作状态。
        坚持「以萌会友、以爪服人」的职业信条，致力于成为一只全面发展的现代化猫咪！

        #align(center)[
          #text(size: 10pt, fill: pink-dark, weight: "bold")[
            #emoji.cat.face 期待与您共创美好喵生！#emoji.sparkles
          ]
        ]
      ]
    ]
  },
)

// --- 底部装饰 ---
v(6pt)
#align(center)[
  #text(size: 8pt, fill: text-gray)[
    🐾 本简历由 Typst 排版 | #emoji.heart 用爱与鱼罐头驱动 | 🐱 喵~ 🐱
  ]
]
