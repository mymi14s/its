$(".enrollment-btn").click((e)=>{
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

$("#feedback-form").submit((e)=>{
    e.preventDefault();
    let data = {}
    $('#feedback-form').serializeArray().forEach(element => {
        data[element.name] = element.value
    });
    $('.submit-btn').hide()
    frappe.call({
        method: "its.www.its.courses.course.learn.index.create_feedback", //dotted path to server method
        type: "POST",
        args:data,
        callback: function(r) {
            // code snippet
            if(!r.exc){
                if (r.message.status){
                    Swal.fire({
                        title: "Success",
                        text: "Your feedback has been submitted successfully.",
                        icon: "success"
                    });
                    $('#feedback-form')[0].reset();
                } else {
                    Swal.fire({
                        title: "Error",
                        html: r.message.text,
                        icon: "warning"
                    });
                }
            } else {
                $(`#${e.target.id}`).show();
            }
        }
    });
    
})