function injectAlignment(toolbar) {
    if (toolbar.querySelector("[name='align_group']")) {
        return;
    }

    const fontSizeGroup = toolbar.querySelector("[name='font-size']");
    if (!fontSizeGroup) return;

    const alignGroup = document.createElement("div");
    alignGroup.classList.add("btn-group");
    alignGroup.setAttribute("name", "align_group");
    alignGroup.innerHTML = `
        <button class="btn btn-light" title="Align left" name="align_left"><span class="fa fa-fw fa-align-left"></span></button>
        <button class="btn btn-light" title="Align center" name="align_center"><span class="fa fa-fw fa-align-center"></span></button>
        <button class="btn btn-light" title="Align right" name="align_right"><span class="fa fa-fw fa-align-right"></span></button>
        <button class="btn btn-light" title="Justify full" name="align_full"><span class="fa fa-fw fa-align-justify"></span></button>
    `;
    fontSizeGroup.insertAdjacentElement("afterend", alignGroup);
}

function startObserver() {
    if (!document.body) {
        setTimeout(startObserver, 100);
        return;
    }

    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1 && node.matches(".o-overlay-item, .o-we-toolbar")) {
                    const toolbar = node.matches(".o-we-toolbar")
                        ? node
                        : node.querySelector(".o-we-toolbar");

                    if (toolbar) {
                        injectAlignment(toolbar);
                        bindAlignment(toolbar);
                    }
                }
            });
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });

    const initialToolbar = document.querySelector(".o-we-toolbar");
    if (initialToolbar) {
        injectAlignment(initialToolbar);
        bindAlignment(initialToolbar);
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startObserver);
} else {
    startObserver();
}

function bindAlignment(toolbar) {
    const buttons = toolbar.querySelectorAll("[name^='align_']");
    buttons.forEach((btn) => {
        btn.addEventListener("click", (ev) => {
            ev.preventDefault();
            let command;
            switch (btn.getAttribute("name")) {
                case "align_left":
                    command = "justifyLeft";
                    break;
                case "align_center":
                    command = "justifyCenter";
                    break;
                case "align_right":
                    command = "justifyRight";
                    break;
                case "align_full":
                    command = "justifyFull";
                    break;
            }
            if (command) {
                document.execCommand(command, false, null);
            }
        });
    });
}

