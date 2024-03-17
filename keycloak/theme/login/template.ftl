<#macro registrationLayout bodyClass="" displayInfo=false displayMessage=true displayRequiredFields=false>
<!DOCTYPE html>
<html class="">

<head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="robots" content="noindex, nofollow">
    <script src="https://cdn.tailwindcss.com?plugins=forms,typography,aspect-ratio,line-clamp"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.6.5/flowbite.min.css" rel="stylesheet" />
    
    <script>
        tailwind.config = {
          theme: {
            extend: {
              colors: {
                "sneaky-yellow": {
                  "50": "#fffce5",
                  "100": "#fef8cd",
                  "200": "#fef29a",
                  "300": "#feec67",
                  "400": "#fde535",
                  "500": "#fcde04",
                  "600": "#e3c702",
                  "700": "#c9b103",
                  "800": "#b19c02",
                  "900": "#968403",
                  "950": "#806c00"
                }
              }
            }
          }
        }
    </script>
    <#if properties.meta?has_content>
        <#list properties.meta?split(' ') as meta>
            <meta name="${meta?split('==')[0]}" content="${meta?split('==')[1]}"/>
        </#list>
    </#if>
    <title>${msg("loginTitle",(realm.displayName!''))}</title>
    <link rel="icon" type="image/png" href="${url.resourcesPath}/img/newsladder.png">
    <#if properties.stylesCommon?has_content>
        <#list properties.stylesCommon?split(' ') as style>
            <link href="${url.resourcesCommonPath}/${style}" rel="stylesheet" />
        </#list>
    </#if>
    <#if properties.styles?has_content>
        <#list properties.styles?split(' ') as style>
            <link href="${url.resourcesPath}/${style}" rel="stylesheet" />
        </#list>
    </#if>
    <#if properties.scripts?has_content>
        <#list properties.scripts?split(' ') as script>
            <script src="${url.resourcesPath}/${script}" type="text/javascript"></script>
        </#list>
    </#if>
    <#if scripts??>
        <#list scripts as script>
            <script src="${script}" type="text/javascript"></script>
        </#list>
    </#if>
</head>

<body class="min-h-screen">
<nav class="w-full border-b">
    <div class="mx-auto max-w-screen-xl px-3 py-3 lg:px-5 lg:pl-3">
        <div class="flex items-center justify-center">
            <div class="flex flex-wrap items-center justify-between bg-white">
                <a href="${properties.frontendurl}" class="flex sm:ml-0">
                    <img
                        
                        src="${url.resourcesPath}/img/newsladder.png"
                        class="mr-3 h-8"
                        alt="fish-and-chips logo"
                    />
                </a>
                <span class="self-center whitespace-nowrap text-xl font-semibold sm:text-2xl"
                    >Newsladder - Authentifizierung</span
                >
            </div>
        </div>
    </div>
</nav>

<div class="flex items-center justify-center">
    <div class="w-full max-w-xl">
        <div class="flex items-center justify-center" style="min-height: 80vh">
            <div
                class="w-full max-w-xl rounded-lg border border-solid border-gray-200 bg-white p-4 shadow shadow-gray-400">
                <div class="space-y-6">
                    <#if realm.internationalizationEnabled  && locale.supported?size gt 1>
                        <div class="">
                            <a href="#">${locale.current}</a>
                            <ul >
                                <#list locale.supported as l>
                                    <li >
                                        <a href="${l.url}">${l.label}</a>
                                    </li>
                                </#list>
                            </ul>
                        </div>
                    </#if>
                    <#if !(auth?has_content && auth.showUsername() && !auth.showResetCredentials())>
                        <#if displayRequiredFields>
                            <div>
                                <div>
                                    <span><span>*</span> ${msg("requiredFields")}</span>
                                </div>
                                <div >
                                    <h1 class="text-xl font-medium text-gray-900"><#nested "header"></h1>
                                </div>
                            </div>
                        <#else>
                            <h1  class="text-xl font-medium text-gray-900"><#nested "header"></h1>
                        </#if>
                    <#else>
                        <#if displayRequiredFields>
                            <div>
                                <div>
                                    <span><span>*</span> ${msg("requiredFields")}</span>
                                </div>
                                <div>
                                    <#nested "show-username">
                                    <label>${auth.attemptedUsername}</label>
                                    <div>
                                        <a href="${url.loginRestartFlowUrl}" aria-label="${msg("restartLoginTooltip")}">
                                            <div >
                                                <i></i>
                                                <span >${msg("restartLoginTooltip")}</span>
                                            </div>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        <#else>
                            <#nested "show-username">
                            <label>${auth.attemptedUsername}</label>
                            <div >
                                <a href="${url.loginRestartFlowUrl}" aria-label="${msg("restartLoginTooltip")}">
                                    <div class="kc-login-tooltip">
                                        <i></i>
                                        <span >${msg("restartLoginTooltip")}</span>
                                    </div>
                                </a>
                            </div>
                        </#if>
                    </#if>
                    <#-- App-initiated actions should not see warning messages about the need to complete the action -->
                    <#-- during login.                                                                               -->
                    <#if displayMessage && message?has_content && (message.type != 'warning' || !isAppInitiatedAction??)>
                        <div class="alert-${message.type} ${properties.kcAlertClass!} pf-m-<#if message.type = 'error'>danger<#else>${message.type}</#if>">
                            <div class="pf-c-alert__icon">
                              <#if message.type = 'success'><span></span></#if>
                              <#if message.type = 'warning'><span></span></#if>
                              <#if message.type = 'error'><span></span></#if>
                              <#if message.type = 'info'><span></span></#if>
                            </div>
                            <span>${kcSanitize(message.summary)?no_esc}</span>
                        </div>
                      </#if>

                    <#nested "form">

                    <#if auth?has_content && auth.showTryAnotherWayLink()>
                        <form action="${url.loginAction}" method="post">
                            <div>
                                <input type="hidden" name="tryAnotherWay" value="on"/>
                                <a href="#" id="try-another-way" onclick="document.forms['kc-select-try-another-way-form'].submit();return false;">${msg("doTryAnotherWay")}</a>
                            </div>
                        </form>
                    </#if>

                    <#nested "socialProviders">

                    <#if displayInfo>
                        <div>
                            <div>
                                <#nested "info">
                            </div>
                        </div>
                    </#if>
                </div>
            <div>
        </div>
    </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.6.5/flowbite.min.js"></script>
</body>
</html>
</#macro>
