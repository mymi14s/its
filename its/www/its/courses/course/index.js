$(".enroll-btn-id").click((e)=>{
    console.log(e)
    enrollFN(e)
})


let enrollFN = (e)=>{
    $(`#${e.target.id}`).hide();
    frappe.call({
        method: "its.www.its.courses.course.index.enroll", //dotted path to server method
        type: "POST",
        args:{educational_content: e.target.id},
        callback: function(r) {
            // code snippet
            if(!r.exc){
                console.log(r)
                if (r.message.status){
                    Swal.fire({
                        title: "Success",
                        text: "Enrollmet successful, you will be redirected.",
                        icon: "success"
                    });
                    setTimeout(()=>{
                        window.location.href = r.message.link
                    }, 3000)
                } else {
                    Swal.fire({
                        title: "Error",
                        html: r.message.text,
                        icon: "warning"
                    });
                    $(`#${e.target.id}`).show();
                }
            } else {
                console.log(r)
                $(`#${e.target.id}`).show();
            }
        }
    });
}