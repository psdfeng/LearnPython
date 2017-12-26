var board = new Array(), //每个格子的数字
    score = 0, //分数
    has_conflicted = new Array(), //解决连续消除的标记
    successString = 'Success',
    gameOverString = 'GameOver';

$("#start").click(function() {
    newGame();
})
$(newGame); //加载完之后开始游戏
function newGame() {
    //初始化数组
    for (var i = 0; i < 4; i++) {
        board[i] = new Array();
        has_conflicted[i] = new Array();
        for (var j = 0; j < 4; j++) {
            board[i][j] = 0;
            has_conflicted[i][j] = false;
        }
    }
    //通过newGame按钮开始游戏时初始化棋盘
    updateBoardView();
    score = 0;
    updateScore(score); //通过newGame按钮开始游戏时初始化分数
    //棋盘上随机出现两个数字
    generateOneNum();
    generateOneNum();
}

//随机一个位置和一个数字
//并将数字显示出来
function generateOneNum() {
    //如果棋盘已满返回
    if (noSpace()) {
        return false;
    }
    var randX, randY, time = 0;
    //最多随机50次
    //保证随机出来的位置上为空
    do {
        time++;
        randX = Math.floor(Math.random() * 4);
        randY = Math.floor(Math.random() * 4);
    } while (board[randX][randY] && (time < 50))
    //50次之后依然随机不到，循环查找空位
    if (time == 50) {
        for (var i = 0; i < 4; i++) {
            for (var j = 0; j < 4; j++) {
                if (!board[i][j]) {
                    randX = i;
                    randY = j;
                }
            }
        }
    }
    //随机出一个数字2或者4
    randNum = Math.random() > 0.1 ? 2 : 4;
    board[randX][randY] = randNum; //设定棋盘上的数字
    showNumAnimate(randX, randY, randNum); //动态显示数字
    return true;
}
//动态显示数字
function showNumAnimate(i, j, randNum) {
    //为目标单元格添加p元素
    var tem = $("tr:eq(" + i + ")").children("td:eq(" + j + ")")
        .append("<p>" + randNum + "</p>")
        .children("p");
    //动态显示数字
    tem.css("background-color", getNumBackcolor(randNum));
    tem.css("color", getNumColor(randNum));
    tem.fadeIn("normal");
}
//根据不同数字显示不同北京颜色
function getNumBackcolor(num) {
    switch (num) {
        case 2:
            return "#eee4da";
            break;
        case 4:
            return "#eee0c8";
            break;
        case 8:
            return '#f2b179';
            break;
        case 16:
            return '#f59563';
            break;
        case 32:
            return '#f67c5f';
            break;
        case 64:
            return '#f65e3b';
            break;
        case 128:
            return '#edcf72';
            break;
        case 256:
            return '#edcc61';
            break;
        case 512:
            return '#9c0';
            break;
        case 1024:
            return '#33b5e5';
            break;
        case 2048:
            return '#09c';
            break;
        case 4096:
            return '#a6c';
            break;
        case 8192:
            return '#93c';
            break;
    }
    return "black";
}
//根据不同数字显示不同字体颜色
function getNumColor(num) {
    if (num > 4) {
        return "snow";
    } else {
        return "#776e65";
    }
}
//重绘棋盘
function updateBoardView() {
    $("td").empty();
    for (var i = 0; i < 4; i++) {
        for (var j = 0; j < 4; j++) {
            if (board[i][j]) {
                var tem = $("tr:eq(" + i + ")").children("td:eq(" + j + ")")
                    .append("<p>" + board[i][j] + "</p>")
                    .children("p");
                tem.css("background-color", getNumBackcolor(board[i][j]));
                tem.css("color", getNumColor(board[i][j]));
                tem.show();
            }
            has_conflicted[i][j] = false;
        }
    }
}

function noSpace() {
    for (var i = 0; i < 4; i++) {
        for (var j = 0; j < 4; j++) {
            if (!board[i][j]) {
                return false;
            }
        }
    }
    return true;
}

function updateScore() {
    $("label>input").attr("value", "" + score);
}