

const pages = [
    { title: "基础信息", text: "内存占用，处理器占用，版本号" },
    { title: "在线设备", text: "正在获取在线设备...", fetch: true },
    { title: "广播测试", text: "这里是广播测试页面。" },
    { title: "接口测试", text: "这里是接口测试页面。" },
    { title: "日志查看", text: "这里是日志查看页面。" },
    { title: "关于我们", text: "请通过邮箱或电话联系我们。" }
];

function loadMarked(cdn) {
    const script = document.createElement('script');
    script.src = cdn;  // 或者你使用的 CDN 地址
    script.onload = function () {
        console.log('marked.js 加载完成');
    };
    script.onerror = function () {
        console.error('加载 marked.js 失败');
    };
    document.head.appendChild(script);
}

loadMarked("https://cdn.jsdelivr.net/npm/markdown-it/dist/markdown-it.min.js");


function changeContent(index) {
    const content = document.getElementById("content");
    content.classList.remove("show");

    setTimeout(() => {
        content.innerHTML = `<h1>${pages[index].title}</h1><p>${pages[index].text}</p>`;
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
    }, 500);
}
function fetchMarkdownFile(content) {
    fetch("/webui/html/readme.md") // 这里 `/about.md` 需替换为实际的 Markdown 文件路径
        .then(response => response.text())
        .then(markdownText => {
            content.innerHTML = `<div id="markdown-content"></div>`;
            const md =window.markdownit({ html: true });;
            const result = md.render(markdownText)
            document.getElementById("markdown-content").innerHTML += result;
        })
        .catch((e) => {
            console.error(e);
            content.innerHTML = `<h1>关于我们</h1><p>加载失败，请稍后再试。</p>`;
        });
}


// 统一获取 CPU、内存、版本信息
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
            datasets: [{ data: [percent, 100 - percent], backgroundColor: colors, hoverOffset: 4 }]
        },
        options: { responsive: true, plugins: { legend: { position: "top" } } }
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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: deviceName })
    })
        .then(response => response.json())
        .then(() => { changeContent(1); })
        .catch(() => { alert(`无法踢出设备 ${deviceName}`); });
}

document.addEventListener("DOMContentLoaded", () => {
    changeContent(0);
});
