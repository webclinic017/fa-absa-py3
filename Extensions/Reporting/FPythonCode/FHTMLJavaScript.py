javaScript = """var childrenArray = new Array();
var rows = document.getElementsByTagName("tr");

function toggleImage(image, rowId, sign)
{
    var img = image;
    if(!img)
    {
        var row = document.getElementById(rowId);
        img = row.getElementsByTagName("img")[0];
    }
    if(sign)
    {
        img.src = "report_" + sign + ".gif";
    }
    else
    {
        img.style.display = "none";
    }
}

function hideRecursive(row, children, checkExpanded)
{
    var child;
    if(children && (row.expanded == "1" || !checkExpanded))
    {
        for(var i = 0; i < children.length; i++)
        {
            child = document.getElementById(children[i]);
            hideRecursive(child, childrenArray[child.id], checkExpanded);
            child.style.display = "none";
        }
    }
}

function showRecursive(row, children)
{
    var child;
    if(children)
    {
        for(var i=0; i < children.length; i++)
        {
            child = document.getElementById(children[i]);
            if(child.expanded == "1")
            {
                showRecursive(child, childrenArray[child.id]);
            }
            if(!childrenArray[child.id])
            {
                toggleImage(0, child.id, "end");
            }
            child.style.display = "block";
        }
    }
}

function onExpandCollapseClick()
{
    var row = document.getElementById(this.rowId);
    var children = childrenArray[this.rowId];
    if(children)
    {
        if(row.expanded == "0")
        {
            toggleImage(this, 0, "minus");
            showRecursive(row, children);
            row.expanded = "1";
        }
        else
        {
            toggleImage(this, 0, "plus");
            hideRecursive(row, children, 1);
            row.expanded = "0";
         }
    }
}

function treeInit()
{
    var image, parentId, depth;
    var parentArray = new Array();
    for(var id = 0; id < rows.length; id++)
    {
        row = rows[id];
        image = row.getElementsByTagName("img")[0];
        if(image)
        {
            depth = row.getAttribute("depth");
            row.id = id;
            image.rowId = id;
            image.onclick = onExpandCollapseClick;
            parentArray[depth] = id;
            if(depth > 1)
            {
                parentId = parentArray[depth - 1];
                row.parentId = parentId;
                if(childrenArray[parentId])
                {
                    childrenArray[parentId].push(id);
                }
                else
                {
                    childrenArray[parentId] = [id];
                }
            }
            row.expanded = "0";
        }
    }
}

function displayInit()
{
    var row, rowId;
    for(var id = 0; id < rows.length; id++)
    {
        row = rows[id];
        rowId = row.id;
        if(rowId && !row.parentId)
        {
            if(childrenArray[rowId])
            {
                hideRecursive(row, childrenArray[rowId], 0);
            }
            else
            {
                toggleImage(0, rowId, 0);
            }
        }
    }
}

function init()
{
    treeInit();
    displayInit();
}"""
