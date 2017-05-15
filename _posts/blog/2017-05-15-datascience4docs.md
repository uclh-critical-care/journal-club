---
layout: post
title: "Datascience for Docs"
categories: blog
excerpt: "A new course to teach data science to clinicians using modern, free open source tools"
tags: [news]
image:
  feature:
date: 2014-08-08T15:39:55-04:00
modified: 2016-06-01T14:19:19-04:00
author: steve_harris
---

## Course organisers

- Dr Steve Harris
- Dr Ahmed al-Hindawi  
- Dr Finn Catling  
- Dr Ed Palmer  
- Dr Danny Wong  

The general public would assume that the medical profession are numerically literate. University-educated, technically-trained in biological science and more, and with the unique legal privilege of prescribing medicines where incorrect dosing leads to disaster, there would seem to be no excuse. However, most medics would deny any affinity with maths, and exude a distaste for statistics. This is a truism even amongst anaesthetists whose professional training includes physics and pharmacokinetics.

Despite this public denial, we are nonetheless a data-literate profession. We read and interpret scientific papers, we run audit projects and write business cases for improvement projects. These are all intrinsically quantitative undertakings. However, our adopted posture gets in the way of our doing these things as well as possible, and engaging with statistics and data.

Data science would appear to be a rebranding of statistics. Despite underpinning quantum mechanics, modern finance, and the humble weather forecast, statistics has never managed to seem cool. At worst, it is cited as ‘lies, damn lies and ...’. However, rename it to data science, chat about machine learning and drop in an ‘artificial neural network’, and you are part of the cool, new tech team.

Moreover, most of the work of a practicing statistician is in preparing data. This is no different to working in a wet lab where the ‘killer’ experiment can’t be done until you have validated your reagents and calibrated your machines. The preparatory must be documented and reproducible for the final table, figure or statistical test to have meaning. The same approach should apply to clinical research, audit and quality improvement.

Such projects typically start with a paper form. Data is then laboriously transcribed into a spreadsheet. You might construct formula, and copy-paste blocks of data to create summaries. New data means repeating the entire process by hand, and when you return to the project, inevitably months later, you struggle to remember your workflow.  More formal analysis requires finding a friendly statistician and a license for SPSS (or another proprietary, menu-driven statistical software package).

We believe that 'data science' actually summarises a much better approach. Very simply it means documenting your work as code. Why code? Not just because it automates the process, but much more importantly it requires you to be precise about what you have done. We believe that with modern, free, open-source tools this is achievable with a very small amount of training. It is with this premise that we created the ['Data Science for Docs'](http://datascibc.org) course.

We teach the concept of a _data pipeline_ so that reproducibility becomes an immediate advantage. A single document, or script, encodes the steps necessary to take data from an online web form into R and out into a report, a simple analysis, or a beautiful data visualisation. When new data is entered, a single key stroke is needed to re-run the entire analysis and update the output. When you come back to your work after a break, the steps required to produce your report are clearly documented. And when you want to share your work, it’s as simple as sending a copy of your code to a collaborator.

The tools necessary to do this work are freely available. Data can be collected on an online form (Google Forms), stored automatically in a Google Sheet, cleaned and analysed in R, and the graphs plotted interactively using online platforms such as Plotly.

We have borrowed heavily from the established and respected Software Carpentry and Data Carpentry courses, that teach a similar approach for scientists from undergraduate to post-docs. However, we focus our course on scenarios (such as audit, surveys, and small clinical research projects) that are a feature of clinical work. This requires care where patient information is being used, but these are surmountable problems not impossible barriers.

Syllabus summary:

- Preliminaries + Motivational Demo
- R for Newbies
- Excel Hell
- Data Pipelines
- Data Wrangling
- Just Enough Statistics
- Data Visualisation

## Conclusion

The course has been supported but the Software Sustainability Institute who pioneered the Software Carpentry and Data Carpentry courses mentioned above, and by our own National Institute of Academic Anaesthesia. We have run the course at a 'hack weekend' where clinicians, biostatisticians, and software engineers worked together using the critical care data from the MIMIC database (Massachusetts Institute of Technology, Boston, USA), and NIHR Critical Care Health Informatics Collaborative (CC-HIC). We have even now run the course in Sri Lanka at the National Intensive Care Skills Training Centre!

The [materials for the course](http://datascibc.org/Data-Science-for-Docs/) are freely available partly because we think this is the ‘right thing’ to do, and partly to provide a reference for people before and after the course. In the coming year, we will extend the course to a two-day format with a ‘bring your own data’ option on the second day. With a very high faculty-to-student ratio, we believe there is a very good chance that delegates will leave not just with a new set of skills, but with a completed analysis.

![](images/dsbc-classroom.jpg)

---

<!--
# Notes

- [x] @TODO: (2017-04-26) 800 words
- [ ] @TODO: (2017-04-26) headshot
- [x] @TODO: (2017-04-26) other authors
- [x] @TODO: (2017-04-26) workshop photo

Pandoc output
pandoc -o out/2017-04-26\ dsbc-rcoa-bulletin.docx --reference-docx=assets/pandoc-reference.docx 2017-04-26\ dsbc-rcoa-bulletin.md


-->
