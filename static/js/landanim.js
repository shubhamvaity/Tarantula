var _0x65c6=['keydown','keyup','mousedown','mouseup','mousemove','touchstart','touchend','start','now','stop','removeEventListener','children','removeChild','dispose','dom','createElement','div','setAttribute','animation','height','load','project','setClearColor','setPixelRatio','devicePixelRatio','gammaInput','gammaOutput','shadows','shadowMap','enabled','appendChild','domElement','setScene','scene','setCamera','parse','camera','player,renderer,scene,camera','stringify','replace','scripts','uuid','APP.Player:\x20Script\x20without\x20object.','length','source','\x0areturn\x20','bind','APP.Player:\x20Event\x20type\x20not\x20supported\x20(','push','init','aspect','width','updateProjectionMatrix','PerspectiveCamera','projectionMatrix','add','VREffect','isAvailable','isLatestAvailable','getMessage','setSize','update','error','stack','updateMatrixWorld','render','play','addEventListener'];(function(_0x501d47,_0x38900a){var _0x2a952a=function(_0x260cd7){while(--_0x260cd7){_0x501d47['push'](_0x501d47['shift']());}};_0x2a952a(++_0x38900a);}(_0x65c6,0x96));var _0x585c=function(_0x47f602,_0x2fb204){_0x47f602=_0x47f602-0x0;var _0x430f99=_0x65c6[_0x47f602];return _0x430f99;};var APP={'Player':function(){var _0x17779e=this;var _0x3a9e84=new THREE['ObjectLoader']();var _0x2766d8,_0x4df837,_0xc6f695;var _0x2de8fe,_0x42dd11,_0x2c222a,_0x4c4009;var _0x4d9c0d={};this[_0x585c('0x0')]=document[_0x585c('0x1')](_0x585c('0x2'));this[_0x585c('0x0')][_0x585c('0x3')]('class',_0x585c('0x4'));this['width']=0x1f4;this[_0x585c('0x5')]=0x1f4;this[_0x585c('0x6')]=function(_0x28ca5c){_0x4c4009=_0x28ca5c[_0x585c('0x7')]['vr'];_0xc6f695=new THREE['WebGLRenderer']({'antialias':!![]});_0xc6f695[_0x585c('0x8')](0x0);_0xc6f695[_0x585c('0x9')](window[_0x585c('0xa')]);if(_0x28ca5c[_0x585c('0x7')][_0x585c('0xb')])_0xc6f695[_0x585c('0xb')]=!![];if(_0x28ca5c[_0x585c('0x7')]['gammaOutput'])_0xc6f695[_0x585c('0xc')]=!![];if(_0x28ca5c[_0x585c('0x7')][_0x585c('0xd')]){_0xc6f695[_0x585c('0xe')][_0x585c('0xf')]=!![];}this[_0x585c('0x0')][_0x585c('0x10')](_0xc6f695[_0x585c('0x11')]);this[_0x585c('0x12')](_0x3a9e84['parse'](_0x28ca5c[_0x585c('0x13')]));this[_0x585c('0x14')](_0x3a9e84[_0x585c('0x15')](_0x28ca5c[_0x585c('0x16')]));_0x4d9c0d={'init':[],'start':[],'stop':[],'keydown':[],'keyup':[],'mousedown':[],'mouseup':[],'mousemove':[],'touchstart':[],'touchend':[],'touchmove':[],'update':[]};var _0x9af4eb=_0x585c('0x17');var _0x4da531={};for(var _0x1b6158 in _0x4d9c0d){_0x9af4eb+=','+_0x1b6158;_0x4da531[_0x1b6158]=_0x1b6158;}var _0x5c4128=JSON[_0x585c('0x18')](_0x4da531)[_0x585c('0x19')](/\"/g,'');for(var _0x5c70b0 in _0x28ca5c[_0x585c('0x1a')]){var _0x4dd8c0=_0x4df837['getObjectByProperty'](_0x585c('0x1b'),_0x5c70b0,!![]);if(_0x4dd8c0===undefined){console['warn'](_0x585c('0x1c'),_0x5c70b0);continue;}var _0x2d0061=_0x28ca5c[_0x585c('0x1a')][_0x5c70b0];for(var _0x94f3a6=0x0;_0x94f3a6<_0x2d0061[_0x585c('0x1d')];_0x94f3a6++){var _0xcfbd57=_0x2d0061[_0x94f3a6];var _0x5b392a=new Function(_0x9af4eb,_0xcfbd57[_0x585c('0x1e')]+_0x585c('0x1f')+_0x5c4128+';')[_0x585c('0x20')](_0x4dd8c0)(this,_0xc6f695,_0x4df837,_0x2766d8);for(var _0x3f6366 in _0x5b392a){if(_0x5b392a[_0x3f6366]===undefined)continue;if(_0x4d9c0d[_0x3f6366]===undefined){console['warn'](_0x585c('0x21'),_0x3f6366,')');continue;}_0x4d9c0d[_0x3f6366][_0x585c('0x22')](_0x5b392a[_0x3f6366][_0x585c('0x20')](_0x4dd8c0));}}}_0x227060(_0x4d9c0d[_0x585c('0x23')],arguments);};this['setCamera']=function(_0x253161){_0x2766d8=_0x253161;_0x2766d8[_0x585c('0x24')]=this[_0x585c('0x25')]/this[_0x585c('0x5')];_0x2766d8[_0x585c('0x26')]();if(_0x4c4009===!![]){_0x2c222a=new THREE[(_0x585c('0x27'))]();_0x2c222a[_0x585c('0x28')]=_0x2766d8[_0x585c('0x28')];_0x2766d8[_0x585c('0x29')](_0x2c222a);_0x2de8fe=new THREE['VRControls'](_0x2c222a);_0x42dd11=new THREE[(_0x585c('0x2a'))](_0xc6f695);if(WEBVR[_0x585c('0x2b')]()===!![]){this[_0x585c('0x0')][_0x585c('0x10')](WEBVR['getButton'](_0x42dd11));}if(WEBVR[_0x585c('0x2c')]()===![]){this[_0x585c('0x0')][_0x585c('0x10')](WEBVR[_0x585c('0x2d')]());}}};this[_0x585c('0x12')]=function(_0x2e95ed){_0x4df837=_0x2e95ed;};this[_0x585c('0x2e')]=function(_0x42ab41,_0x343957){this[_0x585c('0x25')]=_0x42ab41;this['height']=_0x343957;if(_0x2766d8){_0x2766d8[_0x585c('0x24')]=this[_0x585c('0x25')]/this[_0x585c('0x5')];_0x2766d8[_0x585c('0x26')]();}if(_0xc6f695){_0xc6f695[_0x585c('0x2e')](_0x42ab41,_0x343957);}};function _0x227060(_0x20fae0,_0x456bf1){for(var _0x2777b6=0x0,_0x2cfdb3=_0x20fae0[_0x585c('0x1d')];_0x2777b6<_0x2cfdb3;_0x2777b6++){_0x20fae0[_0x2777b6](_0x456bf1);}}var _0x6a2c54,_0x13161a;function _0x1e6360(_0x430097){_0x13161a=requestAnimationFrame(_0x1e6360);try{_0x227060(_0x4d9c0d[_0x585c('0x2f')],{'time':_0x430097,'delta':_0x430097-_0x6a2c54});}catch(_0x25aaec){console[_0x585c('0x30')](_0x25aaec['message']||_0x25aaec,_0x25aaec[_0x585c('0x31')]||'');}if(_0x4c4009===!![]){_0x2766d8[_0x585c('0x32')]();_0x2de8fe['update']();_0x42dd11[_0x585c('0x33')](_0x4df837,_0x2c222a);}else{_0xc6f695[_0x585c('0x33')](_0x4df837,_0x2766d8);}_0x6a2c54=_0x430097;}this[_0x585c('0x34')]=function(){document[_0x585c('0x35')](_0x585c('0x36'),_0x5d99c2);document[_0x585c('0x35')](_0x585c('0x37'),_0xa82697);document[_0x585c('0x35')](_0x585c('0x38'),_0x1db28c);document[_0x585c('0x35')](_0x585c('0x39'),_0x267ac6);document[_0x585c('0x35')](_0x585c('0x3a'),_0x32a8b5);document[_0x585c('0x35')](_0x585c('0x3b'),_0xfe1e9c);document[_0x585c('0x35')](_0x585c('0x3c'),_0x33c015);document[_0x585c('0x35')]('touchmove',_0x4edc7b);_0x227060(_0x4d9c0d[_0x585c('0x3d')],arguments);_0x13161a=requestAnimationFrame(_0x1e6360);_0x6a2c54=performance[_0x585c('0x3e')]();};this[_0x585c('0x3f')]=function(){document[_0x585c('0x40')](_0x585c('0x36'),_0x5d99c2);document[_0x585c('0x40')](_0x585c('0x37'),_0xa82697);document[_0x585c('0x40')](_0x585c('0x38'),_0x1db28c);document[_0x585c('0x40')](_0x585c('0x39'),_0x267ac6);document[_0x585c('0x40')](_0x585c('0x3a'),_0x32a8b5);document['removeEventListener'](_0x585c('0x3b'),_0xfe1e9c);document[_0x585c('0x40')]('touchend',_0x33c015);document[_0x585c('0x40')]('touchmove',_0x4edc7b);_0x227060(_0x4d9c0d['stop'],arguments);cancelAnimationFrame(_0x13161a);};this['dispose']=function(){while(this[_0x585c('0x0')][_0x585c('0x41')][_0x585c('0x1d')]){this[_0x585c('0x0')][_0x585c('0x42')](this[_0x585c('0x0')]['firstChild']);}_0xc6f695[_0x585c('0x43')]();_0x2766d8=undefined;_0x4df837=undefined;_0xc6f695=undefined;};function _0x5d99c2(_0x42e514){_0x227060(_0x4d9c0d[_0x585c('0x36')],_0x42e514);}function _0xa82697(_0x332022){_0x227060(_0x4d9c0d[_0x585c('0x37')],_0x332022);}function _0x1db28c(_0x360a9d){_0x227060(_0x4d9c0d[_0x585c('0x38')],_0x360a9d);}function _0x267ac6(_0x4c8124){_0x227060(_0x4d9c0d[_0x585c('0x39')],_0x4c8124);}function _0x32a8b5(_0x28b590){_0x227060(_0x4d9c0d[_0x585c('0x3a')],_0x28b590);}function _0xfe1e9c(_0xc48e78){_0x227060(_0x4d9c0d[_0x585c('0x3b')],_0xc48e78);}function _0x33c015(_0x17fd31){_0x227060(_0x4d9c0d[_0x585c('0x3c')],_0x17fd31);}function _0x4edc7b(_0x424b51){_0x227060(_0x4d9c0d['touchmove'],_0x424b51);}}};