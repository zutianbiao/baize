function init_code() {
    CodeMirror.fromTextArea(document.getElementById("python_code"), {
        lineNumbers: true,
        matchBrackets: true,
        styleActiveLine: true,
        theme:"ambiance"
    });
    CodeMirror.fromTextArea(document.getElementById("shell_code"), {
        lineNumbers: true,
        matchBrackets: true,
        styleActiveLine: true,
        theme:"ambiance"
    });
}
$(document).ready(function() {
    init_code();
});