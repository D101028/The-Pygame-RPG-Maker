(() => {
    const mainScreen = document.getElementById('mainScreen');

    const blockRows = 10;
    const blockCols = 10;

    const blockWidth = 64;

    const screenWidth = document.documentElement.clientWidth * 0.8;
    const screenHeight = 512;

    mainScreen.style.width = screenWidth + 'px';
    mainScreen.style.height = screenHeight + 'px';

    const gridBorder = 0.5;

    const posText = document.getElementById('posText');

    let isMouseDown = false;
    document.addEventListener('mousedown', () => {
        isMouseDown = true;
    });
    document.addEventListener('mouseup', () => {
        isMouseDown = false;
    });

    const viewSvg = '<svg width="20px" height="20px" style="margin: 5px" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"> <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path> <circle cx="12" cy="12" r="3"></circle> </svg>';
    const hideSvg = '<svg width="20px" height="20px" style="margin: 5px" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"> <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path> <circle cx="12" cy="12" r="3"></circle> <line x1="2" y1="2" x2="22" y2="22"></line> </svg>';

    // current tool: select, draw, erase, (eyedrop)
    let currentTool = 'draw';
    // const selectTool = document.getElementById('selectTool');
    const drawTool = document.getElementById('drawTool');
    // const areaDrawTool = document.getElementById('areaDrawTool');
    const eraseTool = document.getElementById('eraseTool');
    const tools = [drawTool, eraseTool];
    const toolsNames = ['draw', 'erase'];
    // const eyedropTool = document.getElementById('eyedropTool');
    for (let i = 0; i < tools.length; i++) {
        const tool = tools[i];
        const toolName = toolsNames[i];
        tool.addEventListener('click', () => {
            currentTool = toolName;
            for (let tool of tools) {
                tool.className = 'tool-item';
            }
            tool.className = 'tool-item-selected';
        });
    }
    
    // load images
    function createImgAndCrop(path, x = null, y = null, w = null, h = null) { 
        const img = new Image();
        img.src = `/get-image?image_path=${encodeURIComponent(path)}`;
        if (x === null || y === null || w === null || h === null) {
            return img;
        }
        // 創建新的圖像元素
        const croppedImg = new Image();
        img.onload = () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = w;
            canvas.height = h;
            
            // 在 canvas 上繪製圖片的指定區域
            ctx.drawImage(img, x, y, w, h, 0, 0, w, h);
            
            // 設置為裁剪後的圖片
            croppedImg.src = canvas.toDataURL(); // 轉換為 base64
        };
        return croppedImg;
    }
    
    // tile class
    class Tile {
        constructor(code) {
            this.code = code;
            this.repEle = null; // shown in stamp page
            this.sketchEle = null; // shown when sketching
            this.blitEle = null; // shown in canvas
        }
    }

    // tile stamps
    class stampsPage {
        constructor(name) {
            this.name = name;
        }
    }
    
    const stampsContainer = document.getElementById('stampsContainer');
    const stamps = [24, 33, 40, 41, 42, 43, 44, 45, 46, 46, 46];
    let selectedTile = 0;
    const tilesArr = [];
    for (let i = 0; i < stamps.length; i++) {
        const tile = new Tile(i);
        
        const img = createImgAndCrop(`tiles/${stamps[i]}.png`);
        
        tile.repEle = img.cloneNode(true);
        tile.repEle.className = 'rep-img';
        tile.repEle.addEventListener('click', () => {
            for (let j = 0; j < tilesArr.length; j++) {
                tilesArr[j].repEle.className = 'rep-img';
            }
            tile.repEle.className = 'rep-img-selected';
            selectedTile = i;
        });
        stampsContainer.appendChild(tile.repEle);

        tile.sketchEle = img.cloneNode(true);
        tile.sketchEle.className = 'tile-sketch-img';

        tile.blitEle = img.cloneNode(true);
        tile.blitEle.className = 'tile-blit-img';

        tilesArr.push(tile);
    }
    tilesArr[selectedTile].repEle.className = 'rep-img-selected';

    // layer stamps
    const layersContainer = document.getElementById('layersContainer');
    const layers = [];

    class Block {
        constructor(x, y, screen) {
            this.x = x;
            this.y = y;
            this.screen = screen;
            this.ele = document.createElement('div');
            this.ele.className = "block";
            this.ele.style.width = blockWidth + 'px';
            this.ele.style.height = blockWidth + 'px';
            this.ele.style.outline = gridBorder + 'px solid white';
            this.ele.style.left = x * blockWidth + 'px';
            this.ele.style.top = y * blockWidth + 'px';

            this.isMouseEnter = false;

            this.screen.appendChild(this.ele);
            
            this.ele.addEventListener('mouseenter', () => {
                this.ele.className = 'block-hover';
                posText.innerText = `(${this.x}, ${this.y})`;

                // show selected tile
                if (currentTool === 'draw') {
                    const img = tilesArr[selectedTile].sketchEle;
                    img.style.left = this.x * blockWidth + 'px';
                    img.style.top = (this.y + 1) * blockWidth - img.height + 'px';
                    this.screen.appendChild(img);

                    // draw tile
                    if (isMouseDown) {
                        this.drawTile();
                    }
                } else if (currentTool === 'erase') {
                    if (isMouseDown) {
                        this.removeTile();
                    }
                }
            });

            this.ele.addEventListener('mousedown', () => {
                if (currentTool === 'draw') {
                    this.drawTile();
                } else if (currentTool === 'erase') {
                    this.removeTile();
                }
            });

            this.ele.addEventListener('click', () => {
                if (currentTool === 'draw') {
                    this.drawTile();
                } else if (currentTool === 'erase') {
                    this.removeTile();
                }
            });

            this.ele.addEventListener('mouseleave', () => {
                this.ele.className = 'block';
                posText.innerText = 'null';

                // remove shown img
                const img = tilesArr[selectedTile].sketchEle;
                this.screen.removeChild(img);
            });
        }

        drawTile() {
            const layerName = canvas.focusedLayerName;
            if (layerName === null) return ;
            const map = canvas.tilesLayers.get(layerName);
            map.setTile(
                this.x, 
                this.y, 
                selectedTile
            );
        }

        removeTile() {
            const layerName = canvas.focusedLayerName;
            if (layerName === null) return ;
            const map = canvas.tilesLayers.get(layerName);
            map.setTile(
                this.x, 
                this.y, 
                -1
            );
        }
    }

    class TilesLayer {
        constructor(name, width, height, screen, zIndex = 0) {
            this.name = name;
            this.width = width;
            this.height = height;
            this.screen = screen;
            this.map = null;
            this.imgContainerMatrix = null;
            this.frame = null;
            this.zIndex = zIndex;
            this.isHide = false;

            this.initMap();
        }

        initMap() {
            this.map = Array.from({ length: this.height }, () => Array(this.width).fill(-1));
            this.imgContainerMatrix = Array.from({ length: this.height }, () => Array(this.width).fill(null));
            this.frame = document.createElement('div');
            this.frame.style.zIndex = this.zIndex;
            this.screen.appendChild(this.frame);
            for (let i = 0; i < this.width; i++) {
                for (let j = 0; j < this.height; j++) {
                    const imgContainer = document.createElement('div');
                    imgContainer.className = 'tile-img-container';
                    imgContainer.style.zIndex = j * 10 + i;
                    this.imgContainerMatrix[j][i] = imgContainer;
                    this.frame.appendChild(imgContainer);
                }
            }
        }

        setTile(x, y, code) {
            if (x < 0 || x >= this.width || y < 0 || y >= this.height) return ;
            if (this.map[y][x] === code) return ;
            if (code === -1) {
                this.map[y][x] = -1;
                const imgContainer = this.imgContainerMatrix[y][x];
                imgContainer.innerHTML = '';
                return ;
            }
            this.map[y][x] = code;
            const imgContainer = this.imgContainerMatrix[y][x];
            if (imgContainer !== null) {
                const img = tilesArr[code].blitEle.cloneNode(true);
                img.onload = () => {
                    imgContainer.innerHTML = '';
                    imgContainer.style.left = x * blockWidth + 'px';
                    imgContainer.style.top = (y + 1) * blockWidth - img.height + 'px';
                    imgContainer.appendChild(img);
                };
            }
        }
    }
    
    class BGCanvas {
        constructor(screen) {
            this.screen = screen;
            this.ele = document.createElement("div");
            this.ele.className = "canvas"; 
            this.scale = 100; 

            this.blockFrame = null;
            this.blockMatrix = [];

            this.tilesFrame = null;
            this.tilesLayers = new Map();
            this.focusedLayerName = null;

            this.initCanvas(); 
        }

        initCanvas() {
            // init tiles frame
            this.initTilesFrame();

            // init blocks frame
            this.initBlocksFrame();

            // draw canvas
            this.screen.appendChild(this.ele); 
            
            // init resize
            this.resize(100, 0, 0);

            // relocate and fix pos if canvas size < screen size
            let newLeft = 0;
            let newTop = 0;
            if (blockCols * blockWidth * (this.scale / 100) <= screenWidth) {
                newLeft = (screenWidth - blockCols * blockWidth * (this.scale / 100)) / 2;
            }
            if (blockRows * blockWidth * (this.scale / 100) <= screenHeight) {
                newTop = (screenHeight - blockRows * blockWidth * (this.scale / 100)) / 2;
            }
            this.setPos(newLeft, newTop);
        }

        initTilesFrame() {
            // create tiles frame
            this.tilesFrame = document.createElement('div');
            this.tilesFrame.style.position = 'absolute';
            this.tilesFrame.style.zIndex = 0; // bottom layer
            this.ele.appendChild(this.tilesFrame);
        }

        initBlocksFrame() {
            // create block frame
            this.blockFrame = document.createElement('div');
            this.blockFrame.style.position = 'absolute';
            this.blockFrame.style.zIndex = 10000; // top layer
            this.ele.appendChild(this.blockFrame);

            // create blocks
            for (let i = 0; i < blockRows; i++) {
                this.blockMatrix.push([]);
                for (let j = 0; j < blockCols; j++) {
                    const block = new Block(i, j, this.blockFrame);
                    this.blockMatrix[i].push(block);
                }
            }

            // draw outer border
            const outerBorder = document.createElement('div');
            outerBorder.className = 'outer-border';
            outerBorder.style.width = blockCols * blockWidth + 'px';
            outerBorder.style.height = blockRows * blockWidth + 'px';
            outerBorder.style.outline = `${gridBorder * 2}px solid white`;
            this.blockFrame.appendChild(outerBorder);
        }

        addTilesLayer(name, zIndex = 0) {
            const container = document.createElement('div');
            container.className = 'layer-container';

            const tilesLayer = new TilesLayer(name, blockCols, blockRows, this.tilesFrame, zIndex);
            this.tilesLayers.set(name, tilesLayer);

            // create layer rep
            const rep = document.createElement('a');
            rep.className = 'layer-rep';
            rep.innerText = name;
            // // menu
            // const menu = document.createElement('div');
            // menu.className = 'layer-menu';
            // function movedown() {
            //     const index = layers.findIndex((layer) => layer.innerText === name);
            //     if (index === layers.length - 1) return ;
            //     const temp = layers[index].zIndex;
            //     layers[index].zIndex = layers[index + 1].zIndex;
            //     layers[index + 1].zIndex = temp;
            //     layersContainer.insertBefore(layers[index + 1], layers[index]);
            //     layersContainer.insertBefore(layers[index], layers[index + 1]);
            // }
            // function moveup() {
            //     const index = layers.findIndex((layer) => layer.innerText === name);
            //     if (index === 0) return ;
            //     const temp = layers[index].zIndex;
            //     layers[index].zIndex = layers[index - 1].zIndex;
            //     layers[index - 1].zIndex = temp;
            //     layersContainer.insertBefore(layers[index], layers[index - 1]);
            //     layersContainer.insertBefore(layers[index - 1], layers[index]);
            // }
            // const menuContent = document.createElement('ul');
            // const moveDownTag = document.createElement('li');
            // moveDownTag.innerText = 'move down';
            // moveDownTag.addEventListener('click', movedown);
            // const moveUpTag = document.createElement('li');
            // moveUpTag.innerText = 'move up';
            // moveUpTag.addEventListener('click', moveup);
            // menuContent.appendChild(moveDownTag);
            // menuContent.appendChild(moveUpTag);
            // menu.appendChild(menuContent);
            // rep.addEventListener('contextmenu', (event) => {
            //     menu.style.display = "block";
    
            //     // 設置選單位置
            //     menu.style.left = `${event.pageX}px`;
            //     menu.style.top = `${event.pageY}px`;
                
            // });
            // // 點擊外部時隱藏選單
            // document.addEventListener("click", () => {
            //     menu.style.display = "none";
            // });
            rep.addEventListener('click', () => {
                this.selectLayer(name);
            });

            // create hide button
            const hideBtn = document.createElement('div');
            hideBtn.innerHTML = viewSvg;
            hideBtn.className = 'hide-btn';
            hideBtn.addEventListener('click', () => {
                if (!tilesLayer.isHide) {
                    tilesLayer.isHide = true;
                    tilesLayer.frame.style.display = 'none';
                    hideBtn.innerHTML = hideSvg;
                } else {
                    tilesLayer.isHide = false;
                    tilesLayer.frame.style.display = 'block';
                    hideBtn.innerHTML = viewSvg;
                }
            });

            // append
            container.appendChild(rep);
            // container.appendChild(menu);
            container.appendChild(hideBtn);
            layersContainer.appendChild(container);
            layers.push(rep);

            return tilesLayer;
        }

        selectLayer(name) {
            for (let i = 0; i < layers.length; i++) {
                layers[i].className = 'layer-rep';
            }
            this.focusedLayerName = name;
            layers[layers.findIndex((layer) => layer.innerText === name)].className = 'layer-rep-selected';
        }

        getPos() {
            return [
                parseInt(window.getComputedStyle(this.ele).left, 10), 
                parseInt(window.getComputedStyle(this.ele).top, 10)
            ]
        }

        getPosLeft() {
            return parseInt(window.getComputedStyle(this.ele).left, 10);
        }

        getPosTop() {
            return parseInt(window.getComputedStyle(this.ele).top, 10)
        }

        setPos(left = null, top = null) {
            if (top !== null) {
                this.ele.style.top = `${top}px`;
            }
            if (left !== null) {
                this.ele.style.left = `${left}px`;
            }
        }

        resize(scale, mouseX, mouseY) {
            const preScale = this.scale;
            this.ele.style.transformOrigin = `0px 0px`; 
            this.ele.style.transform = `scale(${scale / 100})`; 

            // relocate
            const canvasLeft = this.getPosLeft();
            const canvasTop = this.getPosTop();
            const rect = this.screen.getBoundingClientRect();
            const relativeX = mouseX - rect.left; 
            const relativeY = mouseY - rect.top; 
            const deltaX = (relativeX - canvasLeft) * (scale / preScale - 1);
            const deltaY = (relativeY - canvasTop) * (scale / preScale - 1);
            this.setPos(canvasLeft - deltaX, canvasTop - deltaY);

            this.scale = scale; 

            const newCanvasWidth = blockCols * blockWidth * (this.scale / 100); 
            const newCanvasHeight = blockRows * blockWidth * (this.scale / 100);
            let newLeft = canvasLeft; 
            let newTop = canvasTop; 

            // relocate the canvas pos
            newLeft = this.getPosLeft();
            newTop = this.getPosTop();
            if (newLeft > 0) {
                newLeft = 0;
            } else if (newLeft + newCanvasWidth - screenWidth < 0) {
                newLeft = screenWidth - newCanvasWidth;
            }
            if (newTop > 0) {
                newTop = 0;
            } else if (newTop + newCanvasHeight - screenHeight < 0) {
                newTop = screenHeight - newCanvasHeight;
            }

            // relocate and fix pos if canvas size < screen size
            if (newCanvasWidth <= screenWidth) {
                newLeft = (screenWidth - newCanvasWidth) / 2;
            }
            if (newCanvasHeight <= screenHeight) {
                newTop = (screenHeight - newCanvasHeight) / 2;
            }
            this.setPos(newLeft, newTop);
        }
    }

    // create canvas
    const canvas = new BGCanvas(mainScreen); 

    // disable dragging
    document.addEventListener("dragstart", function(event) {
        event.preventDefault();
    });

    // disable right click
    document.addEventListener('contextmenu', function(event) {
        event.preventDefault(); 
    });

    // customize scrolling
    mainScreen.addEventListener('wheel', function(event) {
        event.preventDefault(); 
        const canvasLeft = canvas.getPosLeft(); 
        const canvasTop = canvas.getPosTop(); 
        const canvasWidth = blockCols * blockWidth * (canvas.scale / 100); 
        const canvasHeight = blockRows * blockWidth * (canvas.scale / 100);
        let newScale = canvas.scale; 

        if (event.ctrlKey) {
            // scaling
            if (event.deltaY < 0) {
                newScale += 20; 
            } else {
                newScale -= 20; 
            }
            // restrict range
            if (newScale <= 10) {
                newScale = 10; 
            } else if (newScale >= 1000) {
                newScale = 1000; 
            }

            canvas.resize(newScale, event.clientX, event.clientY);
            
        } else if (canvasWidth > screenWidth || canvasHeight > screenHeight) {
            const delta = 30;
            // if to fix X or Y 
            const stickX = canvasWidth <= screenWidth;
            const stickY = canvasHeight <= screenHeight;
            let newLeft = canvasLeft;
            let newTop = canvasTop;

            // moving
            if (event.shiftKey) {
                if (event.deltaY < 0 && !stickY) {
                    newLeft = canvasLeft + delta; 
                } else if (event.deltaY > 0 && !stickY) {
                    newLeft = canvasLeft - delta; 
                }
            } else {
                if (event.deltaX < 0 && !stickX) {
                    newLeft = canvasLeft + delta;
                } else if (event.deltaX > 0 && !stickX) {
                    newLeft = canvasLeft - delta;
                } else if (event.deltaY < 0 && !stickY) {
                    newTop = canvasTop + delta;
                } else if (event.deltaY > 0 && !stickY) {
                    newTop = canvasTop - delta;
                }
            }
            
            // restrict range
            if (!stickX) {
                if (newLeft > 0) {
                    newLeft = 0;
                } else if (newLeft + canvasWidth - screenWidth < 0) {
                    newLeft = screenWidth - canvasWidth;
                }
            }
            if (!stickY) {
                if (newTop > 0) {
                    newTop = 0;
                } else if (newTop + canvasHeight - screenHeight < 0) {
                    newTop = screenHeight - canvasHeight;
                }
            }

            canvas.setPos(newLeft, newTop);
        }
    }, { passive: false });
    
    // test map
    let tilesLayer;
    tilesLayer = canvas.addTilesLayer('test', 0);
    tilesLayer.setTile(0, 0, 1);
    tilesLayer.setTile(3, 3, 2);
    tilesLayer = canvas.addTilesLayer('test1lzsodifjsdifjszdofijzsd;foizsjd;fi', 1);
    tilesLayer.setTile(0, 1, 3);
    canvas.selectLayer('test');
})();