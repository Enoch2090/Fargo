![Fargo](Resources/Fargo.png)

## Fargo

Fargo is a CLI tool written in Python. It allows you to watch local show series by typing in the CLI, without the need of remembering which episode to open.

If you are using Windows, just use Pot Player, it has a similar function to what Fargo does. On macOS, Fargo works well with IINA(and that's the only opener this version supports cause I'm lazy).

Feel free to leave other openers that you wish Fargo to support in [issues](https://github.com/Enoch2090/Fargo/issues). Either macOS, Windows or Linux is fine. 

## Installation

```shell
git clone https://github.com/Enoch2090/Fargo.git
pip3 install -r requirements.txt
cd Fargo
python3 setup.py install
```

## Usage

Add:

```shell
fargo add [AliasName] [TargetDirectory]
```

Watch:

```shell
fargo watch [AliasName]
```

Delete:

```shell
fargo delete [AliasName]
```

## Checklist

Fargo is currently a primitive version, so it won't be added to [pypi.org](https://pypi.org).

- [ ] Support for more openers.
- [ ] Record your watching history and sync with [trakt.tv](https://trakt.tv) and [douban.com](https://douban.com).
- [ ] Analysis based on watching history.
- [ ] Commands for redirecting alias names, etc.

## 建立时间不足
你有没有见过一台超频的电脑
二十四小时不间断工作?
周一调休，昨夜电压过低
寄存器都拼命凑足时序
因此每个非门的入口都张贴告示：
漏水，请勿
从此通过

<img src="resources/noPass.JPG" alt="noPass" style="zoom:50%;" />