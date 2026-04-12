// 🐱 可爱小猫简历 - 咪咪 (Mimi)
// Typst 0.14.2

// ========== 页面和全局设置 ==========
#set page(
  paper: "a4",
  margin: (top: 1.5cm, bottom: 1.5cm, left: 1.5cm, right: 1.5cm),
  fill: rgb("#FFF5F5"),
)

#set text(font: ("Noto Sans SC", "Microsoft YaHei", "SimHei"), size: 10pt, fill: rgb("#4A4A4A"))
#set par(leading: 0.8em, justify: true)

// ========== 颜色定义 ==========
#let pink-primary = rgb("#FF6B9D")
#let pink-light = rgb("#FFE0EB")
#let pink-dark = rgb("#D4507A")
#let warm-orange = rgb("#FFB347")
#let warm-yellow = rgb("#FFE066")
#let soft-purple = rgb("#C9B1FF")
#let soft-blue = rgb("#A0D2FF")
#let bg-card = rgb("#FFFFFF")
#let text-dark = rgb("#3D3D3D")
#let text-light = rgb("#7A7A7A")

// ========== 辅助函数 ==========

// 板块标题
#let section-title(title, emoji-icon) = {
  v(0.5em)
  block(width: 100%)[
    #text(size: 14pt, weight: "bold", fill: pink-primary)[#emoji-icon #title]
    #v(-0.3em)
    #line(length: 100%, stroke: 2pt + pink-light)
  ]
  v(0.3em)
}

// 卡片容器
#let card(body) = {
  block(
    width: 100%,
    inset: 12pt,
    radius: 12pt,
    fill: bg-card,
    stroke: 1.5pt + pink-light,
    body
  )
}

// 技能进度条
#let skill-bar(name, level, max-level: 5) = {
  grid(
    columns: (1fr, 2fr),
    gutter: 8pt,
    align(right + horizon, text(size: 9pt, weight: "bold", fill: text-dark)[#name]),
    {
      let filled = level
      let empty = max-level - level
      let dots = ()
      for i in range(filled) {
        dots.push(
          circle(radius: 6pt, fill: pink-primary, stroke: none)
        )
      }
      for i in range(empty) {
        dots.push(
          circle(radius: 6pt, fill: pink-light, stroke: 1pt + pink-primary)
        )
      }
      stack(dir: ltr, spacing: 4pt, ..dots)
    }
  )
}

// 时间线项目
#let timeline-item(period, title, description) = {
  grid(
    columns: (auto, 1fr),
    gutter: 12pt,
    {
      // 时间线圆点和竖线
      align(center)[
        #circle(radius: 5pt, fill: pink-primary, stroke: none)
        #v(-2pt)
        #line(length: 30pt, angle: 90deg, stroke: 1.5pt + pink-light)
      ]
    },
    {
      block(
        width: 100%,
        inset: (left: 0pt, rest: 4pt),
      )[
        #text(size: 8pt, fill: text-light)[#period] \
        #text(size: 10pt, weight: "bold", fill: text-dark)[#title] \
        #text(size: 9pt, fill: text-light)[#description]
      ]
    }
  )
}

// ========== 简历正文 ==========

// ---------- 头部区域 ----------
#block(width: 100%, inset: 16pt, radius: 16pt, fill: gradient.linear(pink-primary, soft-purple, angle: 135deg))[
  #grid(
    columns: (auto, 1fr),
    gutter: 20pt,
    align: horizon,
    // 头像占位 - 圆形
    {
      circle(
        radius: 45pt,
        fill: bg-card,
        stroke: 3pt + white,
      )[
        #align(center + horizon)[
          #text(size: 36pt)[🐱]
        ]
      ]
    },
    // 名字和基本信息
    {
      text(size: 28pt, weight: "bold", fill: white)[咪咪 Mimi]
      linebreak()
      v(4pt)
      text(size: 12pt, fill: rgb("#FFE0EB"))[✨ 英国短毛猫 · 3岁 · 女生]
      linebreak()
      v(2pt)
      text(size: 10pt, fill: rgb("#FFE0EB"))[
        🏠 温暖的家 · 📧 mimi\@catworld.meow · 📱 1388-MEOW-MEOW
      ]
    }
  )
]

#v(0.6em)

// ---------- 双栏布局 ----------
#grid(
  columns: (1fr, 1.8fr),
  gutter: 14pt,

  // ===== 左栏 =====
  {
    // -- 个人简介 --
    section-title("个人简介", "🌸")
    card[
      一只温柔可爱的英短蓝猫，拥有圆圆的大眼睛和软绵绵的毛发。性格温顺但偶尔调皮，擅长在键盘上踩出神秘代码。梦想是吃遍全世界的小鱼干！🐟
    ]

    v(0.6em)

    // -- 技能特长 --
    section-title("技能特长", "⭐")
    card[
      #skill-bar("抓老鼠", 5)
      #v(6pt)
      #skill-bar("卖萌", 5)
      #v(6pt)
      #skill-bar("睡觉", 5)
      #v(6pt)
      #skill-bar("跳跃", 4)
      #v(6pt)
      #skill-bar("撒娇", 5)
      #v(6pt)
      #skill-bar("拆家", 3)
    ]

    v(0.6em)

    // -- 兴趣爱好 --
    section-title("兴趣爱好", "🎀")
    card[
      #grid(
        columns: (1fr, 1fr),
        gutter: 8pt,
        {
          rect(
            width: 100%,
            inset: 8pt,
            radius: 8pt,
            fill: rgb("#FFF0F5"),
            stroke: none,
          )[
            #align(center)[
              #text(size: 16pt)[🧶] \
              #text(size: 8pt, fill: text-dark)[玩毛线球]
            ]
          ]
        },
        {
          rect(
            width: 100%,
            inset: 8pt,
            radius: 8pt,
            fill: rgb("#F0F8FF"),
            stroke: none,
          )[
            #align(center)[
              #text(size: 16pt)[☀️] \
              #text(size: 8pt, fill: text-dark)[晒太阳]
            ]
          ]
        },
        {
          rect(
            width: 100%,
            inset: 8pt,
            radius: 8pt,
            fill: rgb("#FFFFF0"),
            stroke: none,
          )[
            #align(center)[
              #text(size: 16pt)[🐟] \
              #text(size: 8pt, fill: text-dark)[吃小鱼干]
            ]
          ]
        },
        {
          rect(
            width: 100%,
            inset: 8pt,
            radius: 8pt,
            fill: rgb("#F5F0FF"),
            stroke: none,
          )[
            #align(center)[
              #text(size: 16pt)[📦] \
              #text(size: 8pt, fill: text-dark)[钻纸箱]
            ]
          ]
        },
      )
    ]
  },

  // ===== 右栏 =====
  {
    // -- 工作经历 --
    section-title("工作经历", "💼")
    card[
      #timeline-item(
        "2024.01 - 至今",
        "首席卖萌官 (CMO) @ 铲屎官之家",
        "负责每日向铲屎官撒娇，成功率 99.9%。带领团队（1只仓鼠）完成日常巡逻任务。"
      )
      #timeline-item(
        "2023.06 - 2023.12",
        "高级捕鼠专家 @ 阳台安保部",
        "独立完成阳台区域安保工作，驱赶可疑飞虫 200+ 只。获得「最佳警觉奖」。"
      )
      #timeline-item(
        "2023.01 - 2023.05",
        "实习猫咪 @ 猫咖啡厅",
        "为顾客提供治愈服务，客户满意度 100%。专长：呼噜声疗法和踩奶按摩。"
      )
    ]

    v(0.6em)

    // -- 荣誉证书 --
    section-title("荣誉证书", "🏆")
    card[
      #grid(
        columns: (auto, 1fr),
        gutter: 8pt,
        row-gutter: 10pt,
        text(size: 14pt)[🥇], text(size: 9pt, fill: text-dark)[2024 年度 "最可爱猫咪" 金奖],
        text(size: 14pt)[🎖️], text(size: 9pt, fill: text-dark)[连续 365 天 "准时要饭" 打卡成就],
        text(size: 14pt)[📜], text(size: 9pt, fill: text-dark)[国际猫咪联盟 (ICF) 认证血统证书],
        text(size: 14pt)[⭐], text(size: 9pt, fill: text-dark)["踩奶大师" 专业资格认证],
      )
    ]

    v(0.6em)

    // -- 自我评价 --
    section-title("自我评价", "💕")
    card[
      #rect(
        width: 100%,
        inset: 12pt,
        radius: 10pt,
        fill: gradient.linear(rgb("#FFF5F5"), rgb("#F5F0FF"), angle: 90deg),
        stroke: none,
      )[
        #text(size: 9.5pt, fill: text-dark, style: "italic")[
          "我是一只认真负责的好猫咪！虽然偶尔会打翻水杯、咬坏耳机线，但这都是为了测试物品的耐久性。我对小鱼干有着执着的热爱，对工作（睡觉）有着极高的专注度。如果您正在寻找一位兼具颜值与实力的毛茸茸伙伴，请选择我！"
        ]
        #v(6pt)
        #align(right)[
          #text(size: 8pt, fill: text-light)[—— 咪咪 🐾]
        ]
      ]
    ]
  }
)

// ---------- 页脚装饰 ----------
#v(1fr)
#align(center)[
  #text(size: 8pt, fill: text-light)[
    🐾 本简历由咪咪亲自（用爪子）审核 · 用 Typst 排版 · 喵~ 🐾
  ]
]
