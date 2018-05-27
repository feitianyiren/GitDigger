# GitDigger

## GitDigger 是什么？

一个程序员社区，在这里你能从开源项目中挖掘有趣的故事，与其他人分享，让更多人能够知道开源项目、参与改进开源项目，促进开源项目的社区发展。

目前还处于开发阶段，很多功能未完成，如果你是 Python 大佬，可以向此项目提供技术支持，包括但不仅限于：数据库表结构设计、性能优化、代码规范、模块规划、国际化。

## 为何会有 GitDigger？

作为普通开发者，平常无聊的时候会想看看其他人在干什么，长长见识，比如写了什么代码、都在讨论什么问题（Issue）、有哪些有意思的问题和问题评论、哪些项目发布了新版本等等。对于在某些领域有丰富经验的人，可能还会想知道哪些项目正遇到自己擅长领域的问题，看看自己能不能帮上忙。像 GitHub、Bitbucket、GitLab、Coding、码云这类代码平台都专注于源代码托管，用户的认知范围都仅限于自己的项目，没有提供多少途径让用户去发现其它用户和开源项目的动态。

作为开源项目作者或维护者，一个人的时间和精力都是有限的，有时会被一些琐碎的问题浪费很多时间，比如：各种小 bug，添加各种小功能。同类型的问题处理多了会很感到枯燥，但又不得不去做，做多了又会耽误主线任务开发进度，还会浪费动力。当遇到一些大点问题时，会希望有在这块领域的大佬来指点一二，比如：图形绘制算法如何优化、接口如何命名、开源协议是否兼容、怎样写好 README.md、文档怎么组织等问题。自己搜索相关资料比较费时，可能会找不到答案，而去某些问答网站提问的话，需要写详尽的描述，还可能需要提供最小示例，比较麻烦也费时间，还很有可能得不到答案。这只是开发方面，对于普通开发者，不管项目的代码更新得有多频繁，也不会有人知道这个项目，除非主动去推广，通常的推广手段是在各大平台发布版本更新资讯，但持续时间有限，过了一两周又会回到无人问津的状态。

要解决上述问题，需要有个平台能够：

- 挖掘开源项目的各种信息，包括：问题（Issues）、拉取请求（Pull Requests）、评论、发行版（Releases），供用户浏览。
- 展示开源项目及相关的动态，让用户能够方便的找到活跃度高的项目，也能够通过最近动态了解到大家都在干什么。
- 支持让开源项目作者将一些问题（Issue）标记为“需要帮助”来获得更多的曝光，吸引更多有经验的人来向作者提供帮助。

## 它是如何运作的？

开源项目作者从 GitHub 导入项目后，GitDigger 会收集这些项目的相关内容和动态并展示出来，用户如果觉得这些内容有帮助，可以投票，得票数越高的内容排名越靠前，原理和 Hacker News 大致一样，每次投票消耗 1 积分，积分为 0 时不可投票，每日登录奖励 2 积分。

用户可以按话题（Topic）筛选感兴趣的内容，每个话题都有对应的主页，在这个主页可以找到相关的项目、开发者，以及各个项目的动态。

## 运行 GitDigger

### 依赖

GitDigger 依赖于以下软件：

- [Flask](https://github.com/pallets/flask) - a microframework for Python.
- [Flask-Script](https://github.com/smurfix/flask-script) - Flask extension to help writing external scripts for Flask applications.
- [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy) - Adds SQLAlchemy support to Flask.
- [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) - SQLAlchemy database migrations for Flask applications using Alembic
- [Flask-Login](https://github.com/maxcountryman/flask-login) - Flask user session management. 
- [Flask-WTF](https://github.com/lepture/flask-wtf) - Simple integration of Flask and WTForms, including CSRF, file upload and Recaptcha integration.
- [GitHub-Flask](https://github.com/cenkalti/github-flask) - Flask extension for authenticating users with GitHub and making requests to the API. 
- [GitHub-Webhook](https://github.com/bloomberg/python-github-webhook) - A framework for writing webhooks for GitHub, in Python.
- [Psycopg2](https://github.com/psycopg/psycopg2) - PostgreSQL database adapter for the Python programming language.
- [PostgreSQL](https://www.postgresql.org/download/) - The world's most advanced open source database.
- [NodeJS](https://nodejs.org/) - a JavaScript runtime built on Chrome's V8 JavaScript engine.
- [Redis](https://github.com/antirez/redis) - a in-memory database that persists on disk.
- [Celery](https://github.com/celery/celery) - a asynchronous task queue/job queue based on distributed message passing.

Linux 用户可以直接运行 setup.sh 脚本安装这些依赖：

    sh ./setup.sh

### 配置

config 目录下存放着配置文件，其中以下文件需要你按照实际情况来配置：

- github.py - GitHub 应用信息配置
- database.py - 数据库配置

具体示例可参考与它们名称对应的 .example 文件，建议直接复制它们并去掉 .example 后缀名。

### 服务器

如需将此网站部署到线上生产环境中，则需要以下步骤。

修改 `config/nginx/sites-avaliable/gitdigger.com.conf` 文件，将里面的路径改成你的实际路径。之后，复制 config/nginx 目录到 nginx 的配置目录：

    cp -r config/nginx/* /etc/nginx

为配置文件建立软连接，以启动该配置文件：

    ln -s /etc/nginx/sites-available/gitdigger.com.conf /etc/nginx/sites-enabled/gitdigger.com.conf

修改 `config/uwsgi.ini`，将里面的路径改成你的实际路径。之后启动 uwsgi 服务：

    uwsgi --ini config/uwsgi.ini

### 数据库

以 PostgreSQL 为例，先创建 gitdigger 用户：

    sudo -u postgres createuser gitdigger -P

之后为 gitdigger 用户创建 gitdigger_development 数据库：

    sudo -u postgres createdb -O gitdigger gitdigger_development

创建数据库迁移文件，然后升级数据库：

    pipenv run python manage.py db migrate
    pipenv run python manage.py db upgrade

### 任务队列

    celery worker -A app.worker -l info
    celery beat -A app.worker

## 资源

安装 NodeJS 依赖包：

    npm install

构建 CSS、JavaScript 等相关资源文件：

    npm run build

## 启动

先确保 PostgreSQL 和 Redis 服务器已经启动，然后使用以下命令运行网站主程序：

    pipenv run python main.py
