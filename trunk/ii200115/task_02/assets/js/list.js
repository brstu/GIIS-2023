let ab = 
{
    // INIT
    hForm: null, // html форма добавления/редактирования
    hID: null,
    hLogin: null,
    hName: null,
    hEmail: null,
    hTel: null,
    hAddr: null,
    hAbout: null,
    data: [], // записи в адресной книге
    hList: null, // список записей html
    hSearch: null,
    init: () => {

    // ПОЛУЧИТЬ HTML-ЭЛЕМЕНТЫ
    ab.hID = document.querySelector("#abID");
    ab.hForm = document.querySelector("#abForm");
    ab.hLogin = document.querySelector("#abLogin");
    ab.hName = document.querySelector("#abName");
    ab.hEmail = document.querySelector("#abEmail");
    ab.hTel = document.querySelector("#abTel");
    ab.hAddr = document.querySelector("#abAddr");
    ab.hList = document.querySelector("#abList");
    ab.hAbout = document.querySelector("#abAbout");
    ab.hSearch = document.querySelector("#abSearch");

    // ЗАГРУЗИТЬ ЗАПИСИ ИЗ ЛОКАЛЬНОГО ХРАНИЛИЩА
    let data = localStorage.getItem("ab");
    if (data != null)
    {
        ab.data = JSON.parse(data);
    }

    // ВЫВЕСТИ АДРЕСНЫЕ ЗАПИСИ
    ab.draw();
    },

    // ПЕРЕКЛЮЧИТЬ ПОКАЗАТЬ/СКРЫТЬ ФОРМУ ЗАПИСИ
    toggle: (id) =>
    {
    // ЗАКРЫТЬ И СКРЫТЬ
    if (id === false)
    {
        ab.hID.value = "";
        ab.hLogin.value = "";
        ab.hName.value = "";
        ab.hEmail.value = "";
        ab.hTel.value = "";
        ab.hAddr.value = "";
        ab.hAbout.value = "";
        ab.hForm.classList.remove("show");
    }
    // ПОКАЗЫВАТЬ
    else 
    {
        // РЕЖИМ РЕДАКТИРОВАНИЯ
        if (Number.isInteger(id))
        {
            ab.hID.value = id;
            ab.hLogin.value = ab.data[id]["l"];
            ab.hName.value = ab.data[id]["n"];
            ab.hEmail.value = ab.data[id]["e"];
            ab.hTel.value = ab.data[id]["t"];
            ab.hAddr.value = ab.data[id]["a"];
            ab.hAbout.value = ab.data[id]["u"];
        }
        // ПОКАЗАТЬ ФОРМУ ДОБАВЛЕНИЯ/РЕДАКТИРОВАНИЯ
        ab.hForm.classList.add("show");
    }
    },
    
    // СОХРАНИТЬ ВВОД АДРЕСА
    save : () =>
    {
        // ВВОД ДАННЫХ
        let data = 
        {
            l: ab.hLogin.value,
            n: ab.hName.value,
            e: ab.hEmail.value,
            t: ab.hTel.value,
            a: ab.hAddr.value,
            u: ab.hAbout.value
        };

        // ДОБАВИТЬ/ОБНОВИТЬ ЗАПИСЬ
        if (ab.hID.value == "")
        {
            ab.data.push(data);
        }
        else
        {
            ab.data[ab.hID.value] = data;
        }

        // ОБНОВИТЬ ЛОКАЛЬНОЕ ХРАНИЛИЩЕ
        localStorage.setItem("ab", JSON.stringify(ab.data));
        ab.toggle(false);
        ab.draw();
        return false;
    },
    
    // УДАЛИТЬ ЗАПИСЬ АДРЕСА
    del: (id) => 
    {
        if (confirm("Delete Entry?"))
        {
            ab.data.splice(id, 1);
            localStorage.setItem("ab", JSON.stringify(ab.data));
            ab.draw();
        }
    },

    // ВЫВОД ЗАПИСЕЙ В АДРЕСНОЙ КНИГЕ
    draw: () =>
    {
        ab.hList.innerHTML = "";
        for (let i in ab.data)
        {
            let row = document.createElement("div");
            row.className = "row";
            row.innerHTML = 
            `
                <div class="poz">
                    <input type="button" class="material-icons" value="delete" onclick="ab.del(${i})"/>
                    <input type="button" class="material-icons" value="edit" onclick="ab.toggle(${i})"/>
                </div>
                <div>
                    <input class="toggle" type="checkbox" id="collapsible_head_${i}">
                    <label class="lbl_toggle" for="collapsible_head_${i}">
                        <div class="info">
                            <div>
                            <h2 class="login">${ab.data[i]["l"]}</h2>
                                <h3 class="name">${ab.data[i]["n"]}</h3>
                            </div>
                            <div class="arrow"></div>
                        </div>
                    </label>
                    <div class="collapsible_content">
                        <div class="content_inner">
                            <div class="box_one">
                                <div class="mini_box">
                                    <h4 class="name">About</h4>
                                    <hr class="hr_line"/>
                                    <p>${ab.data[i]["u"]}</p>
                                </div>
                            </div>

                            <div class="box_two">
                                <div class="mini_box">
                                    <h4 class="name">Phone</h4>
                                    <hr class="hr_line"/>
                                    <div>${ab.data[i]["t"]}</div>
                                </div>
                                <div class="mini_box">
                                    <h4 class="name">Email</h4>
                                    <hr class="hr_line"/>
                                    <div>${ab.data[i]["e"]}</div>
                                </div>
                                <div class="mini_box">
                                    <h4 class="name">Address</h4>
                                    <hr class="hr_line"/>
                                    <div>${ab.data[i]["a"]}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            ab.hList.appendChild(row);
        }
    },

    search: (val) =>
    {
        ab.hList.innerHTML = "";
        for (let i in ab.data)
        {
            if ((ab.data[i]["l"]).indexOf(val) != -1  || (ab.data[i]["n"]).indexOf(val) != -1)
            {
                
                let row = document.createElement("div");
                row.className = "row";
                row.innerHTML = 
                `
                <div class="poz">
                <input type="button" class="material-icons" value="delete" onclick="ab.del(${i})"/>
                <input type="button" class="material-icons" value="edit" onclick="ab.toggle(${i})"/>
                </div>
                <div>
                <input class="toggle" type="checkbox" id="collapsible_head_${i}">
                <label class="lbl_toggle" for="collapsible_head_${i}">
                <div class="info">
                <div>
                <h2 class="login">${ab.data[i]["l"]}</h2>
                <h3 class="name">${ab.data[i]["n"]}</h3>
                </div>
                <div class="arrow"></div>
                        </div>
                        </label>
                    <div class="collapsible_content">
                        <div class="content_inner">
                            <div class="box_one">
                            <div class="mini_box">
                                    <h4 class="name">About</h4>
                                    <hr class="hr_line"/>
                                    <p>${ab.data[i]["u"]}</p>
                                    </div>
                                    </div>
                                    
                                    <div class="box_two">
                                    <div class="mini_box">
                                    <h4 class="name">Phone</h4>
                                    <hr class="hr_line"/>
                                    <div>${ab.data[i]["t"]}</div>
                                    </div>
                                    <div class="mini_box">
                                    <h4 class="name">Email</h4>
                                    <hr class="hr_line"/>
                                    <div>${ab.data[i]["e"]}</div>
                                    </div>
                                    <div class="mini_box">
                                    <h4 class="name">Address</h4>
                                    <hr class="hr_line"/>
                                    <div>${ab.data[i]["a"]}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>
            `;
            ab.hList.appendChild(row);
            }
        }
    } 

};

window.addEventListener("load", ab.init);

abSearch.oninput = function() 
{
    ab.search(abSearch.value);
};