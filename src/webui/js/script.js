const pages = [
    {title: "基础信息", text: "内存占用，处理器占用，版本号"},
    {title: "在线设备", text: "正在获取在线设备...", fetch: true},
    {title: "广播测试", text: "这里是广播测试页面。"},
    {title: "接口测试", text: "这里是接口测试页面。"},
    {title: "日志查看", text: "这里是日志查看页面。"},
    {title: "关于我们", text: "请通过邮箱或电话联系我们。"}
];

function loadJS(cdn) {
    const script = document.createElement('script');
    script.src = cdn;
    script.onload = function () {
        console.log('marked.js 加载完成');
    };
    script.onerror = function () {
        console.error('加载 marked.js 失败');
    };
    document.head.appendChild(script);
}

function loadCSS(cdn) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = cdn;
    link.onload = function () {
        console.log(`CSS 文件加载完成: ${cdn}`);
    };
    link.onerror = function () {
        console.error(`加载 CSS 失败: ${cdn}`);
    };
    document.head.appendChild(link);
}


loadJS("https://cdn.jsdelivr.net/npm/markdown-it/dist/markdown-it.min.js");
loadJS("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.js")
loadJS("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/mode/javascript/javascript.min.js")
loadJS("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/addon/edit/matchbrackets.min.js")
loadJS("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/addon/edit/matchbrackets.min.js")


loadCSS("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.css");
loadCSS("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/theme/dracula.min.css");



loadCSS("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.css");

function applyCustomCodeMirrorFont() {
    const style = document.createElement("style");
    style.innerHTML = `
        .CodeMirror {
            font-family: 'Fira Code', monospace !important;
            font-size: 14px;
        }
    `;
    document.head.appendChild(style);
}

// 加载 Google 字体，然后应用到 CodeMirror
loadCSS("https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&display=swap");
applyCustomCodeMirrorFont();




function changeContent(index) {
    const content = document.getElementById("content");
    content.classList.remove("show");




    setTimeout(() => {
        if (index === 2) {
            // 广播测试页面
            viewBroPage(content)

        } else {
            content.innerHTML = `<h1>${pages[index].title}</h1><p>${pages[index].text}</p>`;
        }

        content.classList.add("show");

        if (pages[index].fetch) {
            fetchOnlineDevices(content, pages[index].title);
        }

        if (index === 0) {
            fetchSystemInfo(content);
        }
        if (index === 5) {
            fetchMarkdownFile(content);
        }

        if (index === 4) {
            logPage(content);
        }
    }, 500);
}

function sendBroadcast() {
    try {
        const inputContent = editor.getValue().trim(); // 获取 CodeMirror 输入的内容

        if (!inputContent) {
            alert("请输入广播内容！");
            return;
        }

        // 解析 JSON

        const jsonData = JSON.parse(inputContent);

        fetch("/bro", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.text())
        .then(text => {
            alert(text);
        });


    } catch (e) {
        alert("JSON 格式错误，请检查输入内容！");
        console.error("JSON 解析错误：", e);
    }
}



// 加载 markdown 文件
function fetchMarkdownFile(content) {
    fetch("/webui/html/readme.md")
        .then(response => response.text())
        .then(markdownText => {
            content.innerHTML = `<div id="markdown-content"></div>`;
            const md = window.markdownit({html: true});
            const result = md.render(markdownText);
            document.getElementById("markdown-content").innerHTML += result;
        })
        .catch((e) => {
            console.error(e);
            content.innerHTML = `<h1>关于我们</h1><p>加载失败，请稍后再试。</p>`;
        });
}

// 获取 CPU、内存、版本信息
function fetchSystemInfo(content) {
    content.innerHTML = `
        <h1>基础信息</h1>
        <div class="card-container">
            <div class="chart-container">
                <div class="chart-title">CPU 使用情况</div>
                <canvas id="cpuChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">内存使用情况</div>
                <canvas id="memoryChart"></canvas>
            </div>
            <div class="version-container">
                <div class="chart-title">版本信息</div>
                <div id="versionInfo" class="version-info"></div>
            </div>
        </div>
    `;

    fetchCpuInfo();
    fetchMemoryInfo();
    fetchVersionInfo();
}

function fetchCpuInfo() {
    fetch("/get_cpu_info")
        .then(response => response.json())
        .then(data => {
            drawPieChart("cpuChart", data.percent, ["已使用", "空闲"], ["#FF5733", "#4CAF50"]);
        })
        .catch(() => {
            document.getElementById("cpuChart").outerHTML = "<p>获取 CPU 信息失败</p>";
        });
}

function fetchMemoryInfo() {
    fetch("/get_memory_info")
        .then(response => response.json())
        .then(data => {
            drawPieChart("memoryChart", data.percent, ["已使用", "空闲"], ["#007BFF", "#CCCCCC"]);
        })
        .catch(() => {
            document.getElementById("memoryChart").outerHTML = "<p>获取内存信息失败</p>";
        });
}

function fetchVersionInfo() {
    fetch("/get_version_info")
        .then(response => response.json())
        .then(data => {
            document.getElementById("versionInfo").innerHTML = `
                <div class="version-item"><strong>版本号:</strong> ${data.version}</div>
                <div class="version-item"><strong>项目地址:</strong> <a href="${data.source_code_address}" target="_blank">${data.source_code_address}</a></div>
            `;
        })
        .catch(() => {
            document.getElementById("versionInfo").innerHTML = "<p>获取版本信息失败</p>";
        });
}

function drawPieChart(chartId, percent, labels, colors) {
    const ctx = document.getElementById(chartId).getContext("2d");
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{data: [percent, 100 - percent], backgroundColor: colors, hoverOffset: 4}]
        },
        options: {responsive: true, plugins: {legend: {position: "top"}}}
    });
}

// 获取在线设备
function fetchOnlineDevices(content, title) {
    fetch("/get_online_list")
        .then(response => response.json())
        .then(data => {
            const deviceList = data.list.map(device =>
                `<div class="device-card">
                    <h2 title="${device}">${device}</h2>
                    <p><b>在线</b></p>
                    <button class="kick-btn" onclick="kickDevice('${device}')">踢出</button>
                </div>`
            ).join("");

            content.innerHTML = `<h1>${title}</h1><div class="device-list">${deviceList}</div>`;
        })
        .catch(() => {
            content.innerHTML = `<h1>${title}</h1><p>获取数据失败</p>`;
        });
}

// 踢出设备
function kickDevice(deviceName) {
    fetch("/kick", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name: deviceName})
    })
        .then(response => response.json())
        .then(() => {
            changeContent(1);
        })
        .catch(() => {
            alert(`无法踢出设备 ${deviceName}`);
        });
}

document.addEventListener("DOMContentLoaded", () => {
    changeContent(0);
});

function viewBroPage(content) {
    const exampleString = `{
    "pack": [
        {
            "action": "action_name",
            "param": {
                "param1": "aaa",
                "param2": "bbb"
            }
        }
    ]
}`;

    content.innerHTML = `
        <h1>广播测试</h1>
        <br>
        <textarea id="broadcastInput"></textarea>
        <button class="broadcast-btn" onclick="sendBroadcast()">发送广播</button>
    `;

    // 初始化 CodeMirror
    setTimeout(() => {
        window.editor = CodeMirror.fromTextArea(document.getElementById("broadcastInput"), {
            mode: "application/json",   // JSON 语法高亮
            lineNumbers: true,          // 显示行号
            theme: "dracula",           // 代码主题
            matchBrackets: true,        // 匹配括号
            autoCloseBrackets: true,    // 自动闭合括号
        });

        editor.setSize("100%", "500px");  // 设置输入框大小
        editor.setValue(exampleString);   // 设置示例 JSON
    }, 100);
}
let logSocket;
let logContainer = null;
function logPage(content) {
    content.innerHTML = `<h1>日志查看</h1><pre id="log-output"></pre>`;
            logContainer = document.getElementById("log-output");

            if (!logSocket || logSocket.readyState !== WebSocket.OPEN) {
                logSocket = new WebSocket("/ws/log");

                logSocket.onmessage = function (event) {
                    const logData = event.data;
                    logContainer.textContent += logData + "\n"; // 追加日志内容
                    logContainer.scrollTop = logContainer.scrollHeight; // 滚动到底部
                };

                logSocket.onclose = function () {
                    console.log("日志 WebSocket 连接已关闭");
                };

                logSocket.onerror = function (error) {
                    console.error("WebSocket 错误", error);
                };
            }
}