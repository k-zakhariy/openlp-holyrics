### Install requirements
```
pip install -r requirements.txt
```

1. Place exported xml files from OpenLP into songs folder
2. Run `python convert.py`
3. Observe converted songs in `output` folder
4. Pick all files into import dialog 

**Note**: you can add argument to set custom folder name, example:
`python convert.py MySongbook` - will create directory `./output/MySongbook/*.txt`

By default - folder name is `%Y-%m-%d %H:%M` 
