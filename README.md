![Fargo](resources/Fargo.png)

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

<script id="asciicast-KNZmFIkLgjlkrVh9zeqzdTrKV" src="https://asciinema.org/a/KNZmFIkLgjlkrVh9zeqzdTrKV.js" async></script>

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

## Insufficient Setup Time

> Have you seen an overclocked computer  
> run twenty-four hours non-stop?  
> Monday reserved for work,  
> last night suffered from low voltage input  
> All registers struggled to keep synchronized  
> Therefore each NOT gate puts on a notice-  
> Broken pipe, DO NOT  
> passby