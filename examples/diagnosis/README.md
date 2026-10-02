# 从作答到教学调整：三个原创示例

这些材料展示可跳过诊断之后，怎样根据具体作答修改一个学习单元。题目、讲解和模拟作答均为项目原创；课程代码仅说明试点方向，不代表学校官方课件或完整课程覆盖。没有真实学生数据，也没有测得学习效果。

| 学科任务包 | 观察的具体困难 | 阅读顺序 |
| --- | --- | --- |
| ELEC270 方向：信号表示 | 把斜率相消误认为高度归零 | [任务](signals/source.md) → [补讲与复查](signals/teaching-adjustment.md) → [模拟记录](signals/record.json) |
| COMP201 方向：需求分析 | 把逐次限制替换成平均值 | [任务](requirements/source.md) → [补讲与复查](requirements/teaching-adjustment.md) → [模拟记录](requirements/record.json) |
| COMP207 方向：关系数据库 | 把联合主键误解为每列分别唯一 | [任务](relational-keys/source.md) → [补讲与复查](relational-keys/teaching-adjustment.md) → [模拟记录](relational-keys/record.json) |

每包只覆盖一个小目标。记录中的 `e1` 是初次作答，`e2` 是提示后的同题修正，`e3` 是新题作答；所有事件都标为 `synthetic`，没有虚构日期。当前判断只引用新题证据；教学决策保留在新题出现之前的证据截点。延迟题尚未作答，因此保持情况仍未知。讲解文件含复查答案，正式试用应把它留给评阅者，避免提前暴露。

六维观察不必每次填满。学生无需编辑记录文件；没有参加诊断也可以继续建库，已建好的知识库不必迁移。

## 开发者如何复现

在仓库根目录运行，例如：

```sh
python3 skills/stem-study-vault/scripts/learning_tools.py examples/diagnosis/signals/record.json
python3 -m unittest discover -s tests -v
```

如需测试生成行为，让测试者只读取 Skill 和某个包的 `source.md`，在仓库外生成一个单元。按顺序提供模拟作答，不提前提供后续作答或参考讲解；再用 [教学验收表](../../tests/teaching-rubric.md) 检查输出。这里的成品是人工编写的参考示例，不能当作独立代理试跑的结果。

结构检查通过只说明记录符合约定。它不能证明题目评分正确、模型会遵守教学策略，或学生已经学会。
