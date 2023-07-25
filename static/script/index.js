$("#upload-word").click(() => {
    let formData = new FormData
    formData.append('article', $("#input-article").val())
    formData.append('word', $("#input-word").val())
    formData.append('meaning', $("#input-meaning").val())


    fetch('/api/upload/single_word', {
        method: "POST",
        body: formData
    }).then(res => res.json()).then(data => {
        console.log(data)
        let apiResponse = data[1]
        // 등록에 성공했다면
        if (apiResponse === 200) {
            alert(data[0]['msg'])
            window.location.reload()
        }
        // 등록에 실패했다면
        else if (apiResponse === 400) {
            alert(data[0]['msg'])
        }
        else {
            alert('잘못된 접근입니다')
        }
    })
})