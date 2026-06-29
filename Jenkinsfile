/**
 * Jenkins Pipeline — 八爪鱼接口自动化
 * ====================================
 * 触发方式：
 *   1. 定时触发：每天早9点、晚8点
 *   2. GitLab 触发：Push 和 MR 事件
 *   3. 手动触发
 *
 * 需要配置的 Jenkins Credentials（用 Secret Text 类型）：
 *   - octopus-username → 八爪鱼登录手机号
 *   - octopus-password → 八爪鱼登录密码
 *   - dingtalk-webhook  → 钉钉机器人 Webhook（可选）
 *   - feishu-webhook    → 飞书机器人 Webhook（可选）
 *   - mail-to           → 收件人邮箱（可选）
 */
pipeline {
    // ======================== 运行节点 ========================
    // any：任意可用节点（如果公司有内网专有节点，可改为 agent { label '内网' }）
    agent any

    // ======================== 环境变量 ========================
    environment {
        // -------- 八爪鱼认证（从 Jenkins Credentials 读取） --------
        OCTOPUS_BASE_URL = 'http://api.wxorder.taover.com'
        OCTOPUS_USERNAME = credentials('octopus-username')
        OCTOPUS_PASSWORD = credentials('octopus-password')

        // -------- 通知 Webhook（可选，没配也能跑） --------
        DINGTALK_WEBHOOK = credentials('dingtalk-webhook')
        FEISHU_WEBHOOK   = credentials('feishu-webhook')
        MAIL_TO          = credentials('mail-to')

        // -------- Allure 历史趋势（保留多份报告做对比） --------
        ALLURE_HISTORY   = "${WORKSPACE}/allure-history"
    }

    // ======================== 全局选项 ========================
    options {
        timeout(time: 60, unit: 'MINUTES')   // 超时 60 分钟自动终止
        timestamps()                          // 日志加时间戳
        disableConcurrentBuilds()             // 防止并发构建冲突
    }

    // ======================== 触发器 ========================
    triggers {
        cron('0 9,20 * * *')                                    // 定时：每天 9 点、20 点
        gitlab(triggerOnPush: true, triggerOnMergeRequest: true) // GitLab Push/MR 触发
    }

    // ======================== 阶段 ========================
    stages {

        // ------------- 阶段1：拉代码 -------------
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    // 记录触发来源，后续通知会用到
                    env.TRIGGER_TYPE = currentBuild.getBuildCauses()[0].shortDescription ?: 'Manual'
                }
            }
        }

        // ------------- 阶段2：安装依赖 -------------
        stage('Install Dependencies') {
            steps {
                sh '''
                    # uv sync 根据 pyproject.toml + uv.lock 安装所有依赖
                    # --frozen 确保严格用 lock 文件版本，不做依赖解析（更快更稳）
                    uv sync --frozen
                '''
            }
        }

        // ------------- 阶段3：运行测试 -------------
        stage('Run API Tests') {
            steps {
                sh '''
                    # 只跑八爪鱼测试用例
                    # --junitxml：生成 JUnit 格式报告（Jenkins 原生支持）
                    # --alluredir：生成 Allure 原始数据
                    # -v --tb=short：详细输出 + 短堆栈
                    # || true：即使测试失败也不让 Jenkins 停掉，让后续报告阶段能执行
                    uv run pytest tests/test_octopus/ \
                        --junitxml=reports/junit.xml \
                        --alluredir=reports/allure-results \
                        -v --tb=short || true
                '''
            }
        }

        // ------------- 阶段4：生成报告 -------------
        stage('Generate Reports') {
            steps {
                // Allure 报告（带历史趋势对比）
                allure includeProperties: false,
                       results: [[path: 'reports/allure-results']],
                       reportBuildPolicy: 'ALWAYS'

                // JUnit 测试报告（Jenkins 内置，显示测试趋势图）
                junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            }
        }
    }

    // ======================== 后置处理（无论成功失败都执行） ========================
    post {
        always {
            script { notifyAllChannels() }
        }
    }
}

// ============================================================
// 通知封装函数
// 根据构建结果向钉钉 / 飞书 / 邮件发送通知
// ============================================================
def notifyAllChannels() {
    def status   = currentBuild.currentResult
    def duration = currentBuild.durationString.replace(' and counting', '')
    def commitMsg = env.GIT_COMMIT?.take(7) ?: 'N/A'
    def branch   = env.GIT_BRANCH ?: 'unknown'

    // 构建消息模板
    def color = status == 'SUCCESS' ? 'green' : 'red'
    def emoji = status == 'SUCCESS' ? '✅' : '❌'
    def title = "${emoji} 八爪鱼接口自动化 — ${status}"
    def content = """
**分支**：${branch}
**触发**：${env.TRIGGER_TYPE}
**Commit**：${commitMsg}
**耗时**：${duration}
**报告**：[Allure](${env.BUILD_URL}allure/) | [JUnit](${env.BUILD_URL}testReport/)
""".stripIndent()

    // -------- 钉钉通知 --------
    // try-catch 包裹：没配 Webhook 也不影响构建
    try {
        httpRequest(
            url: env.DINGTALK_WEBHOOK,
            httpMode: 'POST',
            contentType: 'APPLICATION_JSON',
            requestBody: """{"msgtype":"markdown","markdown":{"title":"${title}","text":"${content}"}}""",
            validResponseCodes: '200',
            quiet: true               // 忽略 401/404 等返回，不打印异常日志
        )
    } catch (Exception e) {
        echo "钉钉通知跳过（Webhook 未配置或不可达）"
    }

    // -------- 飞书通知 --------
    try {
        httpRequest(
            url: env.FEISHU_WEBHOOK,
            httpMode: 'POST',
            contentType: 'APPLICATION_JSON',
            requestBody: """{"msg_type":"interactive","card":{"header":{"title":{"tag":"plain_text","content":"${title}"},"template":"${color}"},"elements":[{"tag":"markdown","content":"${content}"}]}}""",
            validResponseCodes: '200',
            quiet: true
        )
    } catch (Exception e) {
        echo "飞书通知跳过（Webhook 未配置或不可达）"
    }

    // -------- 邮件通知 --------
    // 成功：只发摘要；失败：附加构建日志
    try {
        emailext(
            subject: "${title} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: content,
            to: env.MAIL_TO,
            mimeType: 'text/html',
            attachLog: status != 'SUCCESS',
            compressLog: true
        )
    } catch (Exception e) {
        echo "邮件通知跳过（未配置或邮件服务不可用）"
    }
}
