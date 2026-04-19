# How we used Claude

### **Accelerating Our Hackathon Project with Claude Code**

In the fast-paced, high-pressure environment of a hackathon, efficiency and rapid iteration are everything. For our latest project, we leaned heavily on Claude Code to accelerate our workflow (and to write this file), and it proved to be an invaluable asset.

**Conquering Exploratory Data Analysis (EDA)**
We primarily used Claude Code to write and structure our Exploratory Data Analysis notebooks. EDA can often become a sprawling, messy process, but Claude was fantastic at managing long-context tasks. Even as our notebooks grew in complexity and we introduced multiple variables and data layers, the model maintained a clear understanding of the broader context, helping us uncover insights faster without losing the thread of our analysis. For some examples of notebooks, refer to:

- ilias/eda.ipynb
- ilias/volatility.ipynb
- yehor/headline_claude_slaving_ipynb

**Agentic Pipeline Implementation**
Beyond just exploration, we utilized Claude to write end-to-end implementations of our data pipelines. We tasked it with handling the entire lifecycle, which included:

* **Data Intake & Preprocessing:** Cleaning and structuring the raw data for analysis.
* **Feature Extraction:** Identifying and pulling the most relevant signals from the dataset.
* **Iterative Evaluation:** Computing our evaluation metrics and automatically refining the approach.

What stood out most was its ability to iterate agentically. Instead of just generating a static block of code, it acted as an active participant in the engineering process—running the data, evaluating the metric, and adjusting the pipeline based on the results. For some examples of colabs that did this:

- ilias/chronos_v1.ipynb
- ilias/chronos_v3.ipynb
- ilias/solution.ipynb

**Finding the Right Direction**
Hackathons are often about navigating ambiguity. More than just a coding assistant, we found Claude Code super useful as a strategic sounding board. Whenever we hit a roadblock or were unsure of the best architectural approach, it reliably pointed us in the right direction, saving us hours of trial and error and allowing us to focus on the core logic of our project.
