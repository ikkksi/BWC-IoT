const pages = [
            {title: "首页", text: "欢迎来到我们的首页！"},
            {title: "关于", text: "我们是一家专注于创新的公司。"},
            {title: "服务", text: "我们提供优质的服务，满足您的需求。"},
            {title: "产品", text: "我们拥有多款高质量的产品。"},
            {title: "联系我们", text: "请通过邮箱或电话联系我们。"}
        ];

function changeContent(index) {
    const content = document.getElementById("content");
    content.classList.remove("show");
    setTimeout(() => {
        content.innerHTML = `<h1>${pages[index].title}</h1><p>${pages[index].text}</p>`;
        content.classList.add("show");
        }, 500);
}