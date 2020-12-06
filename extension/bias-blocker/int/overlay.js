console.log('He is the guardian');

const longVersion = document.createElement('div');
longVersion.innerHTML = getHtml();
document.body.appendChild(longVersion);
setListeners();

const shortVersion = document.createElement('div');
shortVersion.innerHTML = getShortHtml();
shortVersion.style.display = 'none';
console.log('Appended short child on guardian');

let timer = null;


function getShortHtml() {
    return `
        <div class="nobias-ext-short">
            <div id="short-close-btn">
            </div>
        </div>
    `;
}    

function getNobiasContent(articles, tag) {
    let nobiasContent = '';
    for (article of articles) {
        nobiasContent += generateNewsItem({
            title: article.title,
            site: (new URL(article.link)).hostname,
            link: article.link,
            imageUrl: article.image,
            content: article.content,
            tag
        })
    }
    return nobiasContent;
}

function getHtml() {
    return `
        <div class="nobias-wrapper">
            <div class="nobias-confilct">
                Nagorno Karabakh Conflict
            </div>
            <div class="nobias-ext fade-in">
                <div id="long-close-btn"></div>
                <div class="nobias-column" style="border-right: 1px solid var(--cloud_100);">
                    <div id="loader-1" class="nobias-loader" >
                        <img id="img-loader-1" src="https://s8.gifyu.com/images/loaderb0103bfd4ea7a189.gif" width="175"/>
                        <p class="nobias-status">
                            <!--s1-->
                            <!--s1nodata-->
                        </p>
                    </div>                
                    <div class="nobias-header">
                        Azerbaijan
                    </div>
                    <div id="nobias-placeholder-1" style="display:block;" class="nobias-content">
                        <!-- Placeholder1 -->
                    </div>
                    <div id="nobias-content-1" style="display:none;" class="nobias-content">
                        <!-- Content 1 -->
                    </div>
                </div>
                <div id="nobias-right" class="nobias-column">
                    <div id="loader-2" class="nobias-loader">
                        <img id="img-loader-1" src="https://s8.gifyu.com/images/loaderb0103bfd4ea7a189.gif" width="175"/>
                        <p class="nobias-status">
                            <!--s2-->
                            <!--s2nodata-->
                        </p>
                    </div>   
                    <div class="nobias-header">
                        Armenia
                    </div>
                    <div id="nobias-placeholder-2" style="display:block;" class="nobias-content">
                        <!-- Placeholder2 -->
                    </div>
                    <div id="nobias-content-2" style="display:none;" class="nobias-content">
                        <!-- Content 2 -->
                    </div>
                </div>
            </div>
        </div>

    `
}

function generateNewsItem({link, title, site, content, imageUrl, tag}) {
    return `
        <div class="nobias-item ${tag}">
            <div class="nobias-news">
                <div class="nobias-news-header">
                    <a class="nobias-news-link"
                        href="${link}">
                        ${title}
                    </a>
                </div>
                <div class="nobias-news-site">
                    ${site}
                </div>
                <div class="nobias-news-media">
                    <div class="nobias-news-content">
                    ${content}
                    </div>
                    <div class="nobias-news-image">
                        <img src="${imageUrl}" onerror="this.onerror=null; this.src='https://images.squarespace-cdn.com/content/v1/57b9b98a29687f1ef5c622df/1472654514146-SSSPYPQAVO1F9URTI04N/ke17ZwdGBToddI8pDm48kBbOjajeQQtePfd1O4jqnaAUqsxRUqqbr1mOJYKfIPR7LoDQ9mXPOjoJoqy81S2I8N_N4V1vUb5AoIIIbLZhVYxCRW4BPu10St3TBAUQYVKcXMwU3bcPXQlGfZeAHgJ5LFKd7rsAsrvG_OCzJm9yN6vMX6yVKuxxP6-raXwpph8G/republic+square+yerevan?format=1500w'"  width="100%">
                    </div>
                </div>
            </div>
        </div>
    `
}

window.addEventListener('locationchange', function(){
    fetchArticles();
});

function getArticleContent({link, title, site, content, imageUrl}) {
    return `
        <div class="nobias-full-article">
            <div class="nobias-article-header">
                ${title}
            </div>
            <div class="nobias-article-meta">
                <span class="nobias-article-source">
                    ${site}
                </span>
            </div>
            <div class="nobias-article-image">
                <img src="${imageUrl}" />
            </div>
            <div class="nobias-article-content">
                ${content}
            </div>
        </div>
    `;
}

function fetchArticles() {
    fetch('https://rsarticles.herokuapp.com/related_articles/am', {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            "article_date": getPublishDate(), 
            "article_title": getTitle(), 
            "article_text": getContent()
        })
    })
    .then(response => response.json())
    .then(articles => { 
        const nobiasContent = getNobiasContent(articles, 'armenian');
        let newHtml = longVersion.innerHTML.replace('<!-- Placeholder2 -->', nobiasContent);

        if(articles.length > 0) {
            newHtml = newHtml.replace('id="loader-2"', 'id="loader-2" style="display:none;"');
        } else {
            newHtml = newHtml.replace('id="img-loader-2"', 'id="img-loader-2" style="display:none;"');
            newHtml = newHtml.replace('<!--s1nodata-->', 'No articles found');
        }
        longVersion.innerHTML = newHtml;
        const number = 2;
        setTimeout(() => {
            const elements = document.getElementsByClassName("armenian");
            for (let i = 0; i < elements.length; i++) {
                elements[i].addEventListener('click', () => {
                    console.log('Got clicked: ', elements[i]);
                    const article = articles[i];
                    const articleContent = getArticleContent({
                        title: article.title,
                        site: (new URL(article.link)).hostname,
                        link: article.link,
                        imageUrl: article.image,
                        content: article.content
                    });
                    longVersion.innerHTML = longVersion.innerHTML.replace(`id="nobias-placeholder-${number}" style="display:block;"`, `id="nobias-placeholder-${number}" style="display:none;"`);
                    longVersion.innerHTML = longVersion.innerHTML.replace(`id="nobias-content-${number}" style="display:none;"`, `id="nobias-content-${number}" style="display:block;"`);
                    longVersion.innerHTML = longVersion.innerHTML.replace(`<!-- Content ${number} -->`, articleContent);
                }, false);
            }
        }, 1000);
    });

    fetch('https://rsarticles.herokuapp.com/related_articles/az', {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "article_date": getPublishDate(),
            "article_title": getTitle(), 
            "article_text": getContent()
        })
    })
    .then(response => response.json())
    .then(articles => { 
        const nobiasContent = getNobiasContent(articles, 'azeri');
        let newHtml = longVersion.innerHTML.replace('<!-- Placeholder1 -->', nobiasContent);
        if(articles.length > 0) {
            newHtml = newHtml.replace('id="loader-1"', 'id="loader-1" style="display:none;"');
        } else {
            newHtml = newHtml.replace('id="img-loader-1"', 'id="img-loader-1" style="display:none;"');
            newHtml = newHtml.replace('<!--s1nodata-->', 'No articles found');
        }
        longVersion.innerHTML = newHtml;
        const number = 1;
        setTimeout(() => {
            const elements = document.getElementsByClassName("azeri");
            for (let i = 0; i < elements.length; i++) {
                elements[i].addEventListener('click', () => {
                    console.log('Got clicked: ', elements[i]);
                    const article = articles[i];
                    const articleContent = getArticleContent({
                        title: article.title,
                        site: (new URL(article.link)).hostname,
                        link: article.link,
                        imageUrl: article.image,
                        content: article.content
                    });
                    longVersion.innerHTML = longVersion.innerHTML.replace(`id="nobias-placeholder-${number}" style="display:block;"`, `id="nobias-placeholder-${number}" style="display:none;"`);
                    longVersion.innerHTML = longVersion.innerHTML.replace(`id="nobias-content-${number}" style="display:none;"`, `id="nobias-content-${number}" style="display:block;"`);
                    longVersion.innerHTML = longVersion.innerHTML.replace(`<!-- Content ${number} -->`, articleContent);
                }, false);
            }
        }, 1000);
    });
}

setTimeout(() => {
    longVersion.innerHTML = longVersion.innerHTML.replace('<!--s1-->', '<!--s1-->Parsing article...<!--s1-->');
    longVersion.innerHTML = longVersion.innerHTML.replace('<!--s2-->', '<!--s2-->Parsing article...<!--s2-->');
}, 0);

setTimeout(() => {
    longVersion.innerHTML = longVersion.innerHTML.replace('<!--s2-->Parsing article...<!--s2-->', '<!--s2-->Identifying metrics...<!--s2-->');
    longVersion.innerHTML = longVersion.innerHTML.replace('<!--s1-->Parsing article...<!--s1-->', '<!--s1-->Identifying metrics...<!--s1-->');
}, 100);

setTimeout(() => {
    longVersion.innerHTML = longVersion.innerHTML.replace('<!--s2-->Identifying metrics...<!--s2-->', '<!--s2-->Searching first-source news...');
    longVersion.innerHTML = longVersion.innerHTML.replace('<!--s1-->Identifying metrics...<!--s1-->', '<!--s1-->Searching first-source news...');
}, 800);

setTimeout(() => {
    const links = document.getElementsByClassName('content__header');
    let headers = document.getElementsByClassName('content__headline');
    document.querySelectorAll('body p')
        .forEach(element => {
            element.style.backgroundPosition = '-200% 0';
        });
    document.querySelectorAll('h1')
        .forEach(element => {
            element.style.backgroundPosition = '-200% 0';
        });
    document.querySelectorAll('h2')
        .forEach(element => {
            element.style.backgroundPosition = '-200% 0';
        });
    document.querySelectorAll('h3')
        .forEach(element => {
            element.style.backgroundPosition = '-200% 0';
        });
    document.querySelectorAll('h4')
        .forEach(element => {
            element.style.backgroundPosition = '-200% 0';
        });
    document.querySelectorAll('h5')
        .forEach(element => {
            element.style.backgroundPosition = '-200% 0';
        });
    document.querySelectorAll('h6')
        .forEach(element => {
            element.style.backgroundPosition = '-200% 0';
        });
}, 500);

function setListeners(articles, tag, number) {
    document.addEventListener('scroll', function(e) {
        console.log('Start scrolling...');
        longVersion.style.opacity = 0.05;
        //longVersion.style.zIndex = 100000000;
        longVersion.style.animation = null;

        timer = setTimeout(function() {
            longVersion.style.opacity = 1;
            longVersion.style.animation = 'opacityFadeIn ease 0.25s';
            console.log('Finished scrolling...');
        }, 250);
    });    
}

function getTitle() {
    const title = document.querySelector("meta[property='og:title']").getAttribute("content").substr(0, 19);
    return title;
}

function getContent() {
    const content = document.textContent;
    return content;
}

function getPublishDate() {
    const publishDate = document.querySelector("meta[property='article:published_time']").getAttribute("content").substr(0, 19);
    console.log('Publish date: ', publishDate)
    return publishDate;
}

fetchArticles();

