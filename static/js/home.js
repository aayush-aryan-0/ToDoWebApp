document.addEventListener("DOMContentLoaded", function () {
    console.log("JS LOADED");
    const addform = document.getElementById("addForm");
    const deleteform=document.querySelector(".deleteForm");
    const saveform=document.querySelector(".saveForm");
    const status = document.querySelector(".status");


    if (addform) {
        addform.addEventListener("submit", async (e) => {
            e.preventDefault();

            const res = await fetch("/add", { method: "POST" });

            if (!res.ok) {
                setStatus("Add failed", "red");
                return;
            }

            const html = await res.text();

            document.querySelector("main")
                .insertAdjacentHTML("beforeend", html);

            setStatus("Added", "green");
        });
    }


    if (deleteform) {
       deleteform.addEventListener("submit", async(e) => {
        e.preventDefault();
        const formdata=new FormData(e.target);
        const res=await fetch("/delete", { method: "POST" , body:formdata})

        if (res.ok){
            setStatus("DELETED SUCCEFULLY","green");
            deleteform.closest(".taskBox")?.remove();
           
        }
        else{
            setStatus("Delete Failed","red");
        }
         
            
        });
    }

    if (saveform) {
       saveform.addEventListener("submit", async(e) => {
        e.preventDefault();

        
        const formdata=new FormData(e.target);
        const res=await fetch("/save", { method: "POST" , body:formdata})

        if (res.ok){
            setStatus("SAVED","green");
           
        }
        else{
            setStatus("Error Couldn't Save","red");
        }
         
            
        });
    }

    function setStatus(mssg,color){
        status.textContent=mssg;
        status.style.color=color;
        setTimeout(()=>{status.textContent="",status.style.color=""},1000);
    }
});


