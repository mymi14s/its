$(".enrollment-btn").click((e)=>{
    console.log(e)
    assessmentFN(e)
})


let assessmentFN = (e)=>{
    $(`#${e.target.id}`).hide();
    frappe.call({
        method: "its.www.its.courses.course.learn.index.take_assessment", //dotted path to server method
        type: "POST",
        args:{enrollment: e.target.id},
        callback: function(r) {
            // code snippet
            if(!r.exc){
                console.log(r)
                if (r.message.status){
                    Swal.fire({
                        title: "Success",
                        text: "You have completed assessment for this course.",
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