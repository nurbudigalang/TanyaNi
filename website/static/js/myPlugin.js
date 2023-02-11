CKEDITOR.editorConfig = function (config) {
  config.toolbarGroups = [
    { name: 'document', groups: ['document', 'mode', 'doctools'] },
    {
      name: 'editing',
      groups: ['find', 'selection', 'editing', 'spellchecker'],
    },
    { name: 'clipboard', groups: ['clipboard', 'undo'] },
    { name: 'forms', groups: ['forms'] },
    { name: 'basicstyles', groups: ['basicstyles', 'cleanup'] },
    {
      name: 'paragraph',
      groups: ['list', 'indent', 'blocks', 'align', 'bidi', 'paragraph'],
    },
    { name: 'links', groups: ['links'] },
    { name: 'insert', groups: ['insert'] },
    '/',
    '/',
    { name: 'styles', groups: ['styles'] },
    { name: 'colors', groups: ['colors'] },
    { name: 'tools', groups: ['tools'] },
    { name: 'others', groups: ['others'] },
    { name: 'about', groups: ['about'] },
  ];

  config.removeButtons =
    'Print,Save,NewPage,ExportPdf,Preview,Source,Templates,Cut,Copy,Paste,PasteText,PasteFromWord,Find,Replace,SelectAll,Scayt,Form,Checkbox,Radio,TextField,Textarea,Select,Button,ImageButton,HiddenField,CreateDiv,BidiLtr,BidiRtl,Language,Anchor,Table,HorizontalRule,Smiley,SpecialChar,PageBreak,Iframe,BGColor,TextColor,About';
};
