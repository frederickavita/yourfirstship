from browser import html, document, window

class UI:
    """
    KIT UI COMPLET POUR BRYTHON + TAILWIND CSS.
    Composants : Layouts, Boutons, Badges, Breadcrumbs, Accordéons, Arbres de fichiers, Modales.
    """

    # ==========================================
    # 1. CONFIGURATION (THÈME & ICÔNES)
    # ==========================================
    
    THEME = {
        # Couleurs de fond
        "app_bg":      "bg-slate-900",
        "sidebar_bg":  "bg-slate-950",
        "panel_bg":    "bg-slate-800",
        "input_bg":    "bg-slate-950",
        
        # Bordures & Formes
        "border":      "border-slate-700",
        "radius":      "rounded-md",
        
        # Texte
        "text_main":   "text-slate-200",
        "text_muted":  "text-slate-400",
        
        # Actions & États
        "accent":      "blue",   # ex: text-blue-500
        "danger":      "red",
        "success":     "emerald",
        "warning":     "amber",
        "hover":       "hover:bg-white/5",
    }

    # Icônes SVG (Path data)
    ICONS = {
        "settings": "M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.09a2 2 0 0 1-1-1.74v-.47a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
        "check": "M9 12.75L11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z",
        "chat": "M8.625 9.75a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 0 1 .778-.332 48.294 48.294 0 0 0 5.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z",
        "home": "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6",
        "chevron_right": "M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z",
        "slash": "m9 20.247 6-16.5",
        "x": "M18 6L6 18M6 6l12 12",
        "play": "M5 3l14 9-14 9V3z",
        "save": "M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z M17 21v-8H7v8M7 3v5h8V3",
        "file": "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z M13 2v7h7",
        "folder": "M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z",
        "python": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z",
        "trash": "M3 6h18 M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
    }

    # ==========================================
    # 2. HELPERS (UTILITAIRES)
    # ==========================================

    @staticmethod
    def Icon(name_or_path, size=20, extra_class=""):
        """Génère un SVG (soit depuis ICONS, soit path brut)."""
        d = UI.ICONS.get(name_or_path, name_or_path)
        return html.SVG(
            html.PATH(d=d, stroke_linecap="round", stroke_linejoin="round", stroke_width="2"),
            xmlns="http://www.w3.org/2000/svg", viewBox="0 0 24 24", fill="none", stroke="currentColor",
            width=size, height=size, Class=f"inline-block {extra_class}"
        )

    @staticmethod
    def _get_color(key):
        return UI.THEME.get(key, key)

    # ==========================================
    # 3. LAYOUTS & CONTAINERS
    # ==========================================

    @staticmethod
    def IDE_Layout():
        """Layout principal de l'IDE."""
        t = UI.THEME
        root = html.DIV(Class=f"flex h-screen w-screen {t['app_bg']} {t['text_main']} overflow-hidden font-sans")
        
        sidebar = html.ASIDE(Class=f"w-64 {t['sidebar_bg']} border-r {t['border']} flex flex-col transition-all duration-300")
        main_area = html.MAIN(Class="flex-1 flex flex-col min-w-0")
        
        top_bar = html.HEADER(Class=f"h-12 {t['app_bg']} border-b {t['border']} flex items-center px-4 justify-between")
        
        content_split = html.DIV(Class="flex-1 flex flex-col relative")
        editor_zone = html.DIV(Class=f"flex-1 relative {t['app_bg']} overflow-hidden", Id="editor-container")
        terminal_zone = html.DIV(Class=f"h-48 {t['sidebar_bg']} border-t {t['border']} flex flex-col", Id="terminal-container")
        
        status_bar = html.FOOTER(Class=f"h-6 bg-{t['accent']}-900 text-xs flex items-center px-3 select-none text-{t['accent']}-200")

        content_split <= editor_zone
        content_split <= terminal_zone
        main_area <= top_bar
        main_area <= content_split
        main_area <= status_bar
        root <= sidebar
        root <= main_area

        return {"root": root, "sidebar": sidebar, "top_bar": top_bar, "editor": editor_zone, "terminal": terminal_zone, "status": status_bar}

    @staticmethod
    def Panel(title=None, items=None, extra_class=""):
        t = UI.THEME
        panel = html.DIV(Class=f"{t['panel_bg']} border {t['border']} {t['radius']} overflow-hidden flex flex-col {extra_class}")
        if title:
            panel <= html.DIV(title, Class=f"px-3 py-2 bg-black/20 border-b {t['border']} text-xs font-bold uppercase {t['text_muted']}")
        content = html.DIV(Class="p-0 flex-1 relative")
        if items:
            for item in items: content <= item
        panel <= content
        return panel

    @staticmethod
    def GlassPanel(children, extra_class=""):
        """Panneau style 'Glassmorphism' sombre."""
        panel = html.DIV(Class=f"bg-gray-900/90 border border-gray-700 shadow-2xl rounded-xl overflow-hidden {extra_class}")
        if isinstance(children, list):
            for child in children: panel <= child
        else:
            panel <= children
        return panel

   # ==========================================
    # 4. COMPOSANTS ATOMIQUES (BOUTONS)
    # ==========================================

    @staticmethod
    def Button(text, href=None, variant="primary", size="md", icon=None, icon_pos="left", width="auto", onclick=None, extra_class=""):
        """
        Bouton polyvalent (Lien ou Action).
        
        Args:
            text: Libellé du bouton.
            href: Si présent, rend un <a>, sinon un <button>.
            variant: 
                - "primary": Fond couleur accent.
                - "secondary" / "outline": Bordure couleur accent.
                - "ghost": Transparent.
                - "gradient": Bordure dégradée.
                - "3d": Effet rétro décalé.
            size: "sm", "md", "lg".
            icon: Nom de l'icône (ex: "download").
            icon_pos: "left" ou "right".
            width: "auto" ou "full".
        """
        t = UI.THEME
        
        # Choix du tag
        tag = html.A if href else html.BUTTON
        attrs = {"href": href} if href else {"type": "button"}
        
        # Dimensions
        sizes = {
            "sm": "px-4 py-2 text-xs",
            "md": "px-6 py-3 text-sm",
            "lg": "px-8 py-4 text-base"
        }
        sz_cls = sizes.get(size, sizes["md"])
        w_cls = "w-full block text-center" if width == "full" else "inline-block"
        
        # --- Construction selon Variant ---
        
        # 1. Variant: 3D (Artistic Offset)
        if variant == "3d":
            # Structure complexe: Un wrapper relatif + 2 spans
            container = html.A(href=href, Class=f"group relative {w_cls} {extra_class}") if href else html.BUTTON(type="button", Class=f"group relative {w_cls} {extra_class}")
            
            # L'ombre (Span arrière)
            shadow = html.SPAN(Class=f"absolute inset-0 translate-x-1.5 translate-y-1.5 bg-{t['accent']}-300 transition-transform group-hover:translate-x-0 group-hover:translate-y-0")
            
            # Le bouton (Span avant)
            front = html.SPAN(Class=f"relative inline-flex items-center justify-center gap-2 border-2 border-current {t['panel_bg']} {sz_cls} font-bold tracking-widest text-black dark:text-white uppercase")
            
            if icon and icon_pos == "left": front <= UI.Icon(icon, size=18)
            front <= html.SPAN(text)
            if icon and icon_pos == "right": front <= UI.Icon(icon, size=18)
            
            container <= shadow
            container <= front
            if onclick: container.bind("click", onclick)
            return container

        # 2. Variant: Gradient (Border)
        elif variant == "gradient":
            # Structure: Wrapper avec background gradient + Span interne blanc
            grad_cls = f"bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 p-[2px] hover:text-white focus:outline-none focus:ring active:text-opacity-75"
            base_node = tag(Class=f"group {w_cls} rounded-full {grad_cls} {extra_class}", **attrs)
            
            inner = html.SPAN(Class=f"block rounded-full {t['panel_bg']} {sz_cls} font-medium group-hover:bg-transparent transition-colors flex items-center justify-center gap-2")
            
            if icon and icon_pos == "left": inner <= UI.Icon(icon, size=18)
            inner <= html.SPAN(text)
            if icon and icon_pos == "right": inner <= UI.Icon(icon, size=18)
            
            base_node <= inner
            if onclick: base_node.bind("click", onclick)
            return base_node

        # 3. Variants Standards (Primary, Secondary, Ghost)
        else:
            base_cls = f"{w_cls} {sz_cls} font-medium transition-all focus:outline-none focus:ring active:text-opacity-75 flex items-center justify-center gap-2"
            
            if variant == "primary":
                # Solid
                style_cls = f"rounded border border-{t['accent']}-600 bg-{t['accent']}-600 text-white hover:bg-transparent hover:text-{t['accent']}-600"
            elif variant == "outline" or variant == "secondary":
                # Bordered
                style_cls = f"rounded border border-{t['accent']}-600 text-{t['accent']}-600 hover:bg-{t['accent']}-600 hover:text-white"
            elif variant == "ghost":
                # Transparent
                style_cls = f"text-{t['accent']}-600 hover:bg-{t['accent']}-50 dark:hover:bg-{t['accent']}-900/20"
            else:
                style_cls = ""

            # Effets Hover (Scale, Rotate) via extra_class si besoin
            # Mais on ajoute un défaut sympa pour primary
            if variant == "primary": extra_class += " hover:shadow-lg"

            btn = tag(Class=f"{base_cls} {style_cls} {extra_class}", **attrs)
            
            if icon and icon_pos == "left": btn <= UI.Icon(icon, size=18)
            btn <= html.SPAN(text)
            if icon and icon_pos == "right": btn <= UI.Icon(icon, size=18)
            
            if onclick: btn.bind("click", onclick)
            return btn

    @staticmethod
    def ButtonGroup(buttons, extra_class=""):
        """Groupe de boutons attachés."""
        container = html.SPAN(Class=f"inline-flex -space-x-px overflow-hidden rounded-md border {UI.THEME['border']} shadow-sm {extra_class}")
        
        for i, b_data in enumerate(buttons):
            # b_data: {'icon': 'edit', 'onclick': cb}
            btn = html.BUTTON(
                Class=f"inline-block px-4 py-2 text-sm font-medium {UI.THEME['text_muted']} hover:bg-gray-50 focus:relative dark:hover:bg-gray-800 transition-colors"
            )
            if b_data.get("icon"):
                btn <= UI.Icon(b_data["icon"], size=16)
            if b_data.get("onclick"):
                btn.bind("click", b_data["onclick"])
            container <= btn
            
        return container
    # ==========================================
    # 5. COMPOSANTS COMPLEXES : BADGES
    # ==========================================

    @staticmethod
    def Badge(text="", icon=None, color="accent", filled=True, on_dismiss=None, extra_class=""):
        """
        Badge polyvalent (Texte, Icône, Dismissible).
        Correspond aux styles 'Base', 'Icon', 'Dismiss' de HyperUI.
        
        Args:
            text: Texte du badge.
            icon: Nom de l'icône (clé UI.ICONS) ou path SVG.
            color: Nom de couleur Tailwind (purple, emerald, amber, red) ou clé du thème (accent, danger).
            filled: True (fond plein) / False (bordure).
            on_dismiss: Fonction appelée au clic sur la croix.
        """
        t = UI.THEME
        
        # Résolution de la couleur (ex: 'accent' -> 'blue', 'danger' -> 'red')
        c = UI.THEME.get(color, color) 
        
        # Base shape (rounded-full pour le style 'pill')
        base_cls = "inline-flex items-center justify-center rounded-full px-2.5 py-0.5 text-sm font-medium whitespace-nowrap transition-colors"
        
        # Gestion des styles (Mode Sombre natif à l'IDE)
        # On utilise des teintes adaptées au fond sombre (700/100 ou border/text-100)
        if filled:
            # Style Filled Dark : bg-purple-700 text-purple-100
            style_cls = f"bg-{c}-700 text-{c}-100"
        else:
            # Style Outline Dark : border border-purple-500 text-purple-100
            style_cls = f"bg-transparent border border-{c}-500 text-{c}-100"
            
        badge = html.SPAN(Class=f"{base_cls} {style_cls} {extra_class}")
        
        # 1. Icône (Gauche)
        if icon:
            # Ajustement des marges si texte présent ou non
            margin = "-ms-1 me-1.5" if text else ""
            # L'icône hérite de la couleur du texte (text-purple-100)
            badge <= UI.Icon(icon, size=16, extra_class=f"{margin} opacity-90") # size-4 = 16px

        # 2. Texte
        if text:
            badge <= html.SPAN(text)
            
        # 3. Bouton Dismiss (Droite)
        if on_dismiss:
            # Style du bouton fermer adapté au badge sombre
            # Hover : on éclaircit légèrement le fond du bouton
            btn_cls = f"ms-1.5 -me-1 inline-flex rounded-full bg-{c}-800 p-0.5 text-{c}-100 transition hover:bg-{c}-900 focus:outline-none"
            
            btn = html.BUTTON(Class=btn_cls, title="Supprimer")
            btn <= html.SPAN("Remove", Class="sr-only")
            btn <= UI.Icon("x", size=12) # size-3 = 12px
            
            def _handle_click(ev):
                ev.stopPropagation()
                on_dismiss()
                badge.remove()
                
            btn.bind("click", _handle_click)
            badge <= btn
            
        return badge

    # ==========================================
    # 6. MÉTHODES CONVENIENCE (BADGES PRÉDÉFINIS)
    # ==========================================

    @staticmethod
    def BadgeLive(filled=True, **kwargs):
        """Badge 'Live' (Violet)."""
        return UI.Badge("Live", color="purple", filled=filled, **kwargs)

    @staticmethod
    def BadgeEuro(filled=True, **kwargs):
        """Badge 'Euro' avec icône devise."""
        # Icône Euro spécifique
        path = "M14.25 7.756a4.5 4.5 0 100 8.488M7.5 10.5h5.25m-5.25 3h5.25M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        return UI.Badge("Euro", icon=path, color="purple", filled=filled, **kwargs)

    @staticmethod
    def BadgeSuccess(text="Paid", filled=True, **kwargs):
        """Badge Succès (Emerald)."""
        return UI.Badge(text, icon="check", color="emerald", filled=filled, **kwargs)

    @staticmethod
    def BadgeWarning(text="Refunded", filled=True, **kwargs):
        """Badge Attention (Amber)."""
        # Icône 'Refunded' (flèches circulaires ou horloge)
        path = "M8.25 9.75h4.875a2.625 2.625 0 010 5.25H12M8.25 9.75L10.5 7.5M8.25 9.75L10.5 12m9-7.243V21.75l-3.75-1.5-3.75 1.5-3.75-1.5-3.75 1.5V4.757c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0c1.1.128 1.907 1.077 1.907 2.185z"
        return UI.Badge(text, icon=path, color="amber", filled=filled, **kwargs)

    @staticmethod
    def BadgeDanger(text="Failed", filled=True, **kwargs):
        """Badge Erreur (Red)."""
        # Icône 'Failed' (exclamation ou croix cercle)
        path = "M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
        return UI.Badge(text, icon=path, color="red", filled=filled, **kwargs)

    # ==========================================
    # 6. COMPOSANTS COMPLEXES : BREADCRUMBS
    # ==========================================

    @staticmethod
    def Breadcrumb(items, divider="chevron", home_icon=False, extra_class=""):
        """
        Fil d'Ariane classique (transparent).
        Gère les styles : Base, Slash, Chevron, Home Icon.
        """
        t = UI.THEME
        nav = html.NAV(aria_label="Breadcrumb")
        ol = html.OL(Class=f"flex items-center gap-1 text-sm {t['text_muted']} {extra_class}")
        
        # Choix de l'icône de séparation
        sep_icon = "chevron_right" if divider == "chevron" else "slash"
        
        for i, item_data in enumerate(items):
            label, url = item_data[0], item_data[1]
            callback = item_data[2] if len(item_data) > 2 else None
            
            li = html.LI(Class="flex items-center")
            
            # Styles liens
            link_cls = f"block transition-colors hover:{t['text_main']}"
            if i == len(items) - 1: # Dernier élément (actif)
                link_cls = f"block font-medium {t['text_main']} pointer-events-none"
            
            link = html.A(href=url, Class=link_cls)
            if callback: link.bind("click", callback)
            
            # Gestion Home Icon (seulement sur le premier élément)
            if i == 0 and home_icon:
                link <= UI.Icon("home", size=16)
                # Afficher le label seulement si ce n'est pas "Home" (pour éviter redondance)
                if label.lower() != "home": 
                    # Petit wrapper pour aligner icône + texte
                    span = html.SPAN(label, Class="ms-2")
                    link.clear() # On vide pour remettre icône + texte propre
                    link <= UI.Icon("home", size=16)
                    link <= span
                    link.classList.add("flex", "items-center")
            else:
                link <= html.SPAN(label)
                
            li <= link
            
            # Ajout du séparateur APRES l'élément (sauf le dernier)
            if i < len(items) - 1:
                # Le séparateur est dans son propre LI pour respecter la sémantique HyperUI
                sep_li = html.LI(Class="rtl:rotate-180")
                sep_li <= UI.Icon(sep_icon, size=16) # size-4 = 16px
                ol <= li
                ol <= sep_li
            else:
                ol <= li
                
        nav <= ol
        return nav

    @staticmethod
    def BreadcrumbGrouped(items, extra_class=""):
        """
        Fil d'Ariane style 'Barre d'onglets' (Grouped with chevron divider).
        Utilise clip-path pour les flèches.
        """
        t = UI.THEME
        nav = html.NAV(aria_label="Breadcrumb")
        
        # Conteneur principal avec bordures et fond
        ol = html.OL(
            Class=f"flex overflow-hidden {t['radius']} border {t['border']} "
                  f"{t['panel_bg']} text-sm {t['text_muted']} {extra_class}"
        )
        
        for i, item_data in enumerate(items):
            label, url = item_data[0], item_data[1]
            callback = item_data[2] if len(item_data) > 2 else None
            
            li = html.LI(Class="relative flex items-center")
            
            # 1. Flèche CSS (Triangle) pour les éléments après le premier
            if i > 0:
                # Le triangle de fond
                arrow = html.SPAN(
                    Class=f"absolute inset-y-0 -start-px h-10 w-4 "
                          f"bg-{t['accent']}-900/10 " # Couleur légèrement différente pour le contraste
                          f"[clip-path:polygon(0_0,_0%_100%,_100%_50%)] rtl:rotate-180 z-10"
                )
                li <= arrow
                padding = "ps-8 pe-4"
            else:
                padding = "px-4"
            
            # 2. Lien
            # Style : h-10 pour hauteur fixe, leading-10 pour centrer verticalement
            link = html.A(
                label,
                href=url,
                Class=f"flex items-center h-10 {padding} leading-10 transition-colors "
                      f"hover:{t['text_main']} hover:bg-{t['accent']}-900/20"
            )
            
            # Style actif pour le dernier élément ?
            if i == len(items) - 1:
                link.classList.add(t['text_main'], "font-medium")
            
            if callback: link.bind("click", callback)
            
            li <= link
            ol <= li
            
        nav <= ol
        return nav
    

    # ==========================================
    # 7. COMPOSANTS COMPLEXES : ACCORDÉONS
    # ==========================================

    @staticmethod
    def AccordionBase(items, extra_class=""):
        t = UI.THEME
        container = html.DIV(Class=f"space-y-2 {extra_class}")
        for title, content in items:
            details = html.DETAILS(Class="group [&_summary::-webkit-details-marker]:hidden")
            summary = html.SUMMARY(Class=f"flex cursor-pointer items-center justify-between gap-4 {t['radius']} border {t['border']} {t['panel_bg']} px-4 py-3 font-medium {t['text_main']} hover:{t['hover']} transition-colors")
            summary <= html.SPAN(title)
            summary <= UI.Icon("M19 9l-7 7-7-7", size=20, extra_class=f"shrink-0 transition-transform duration-300 group-open:-rotate-180 {t['text_muted']}")
            
            content_div = html.DIV(Class=f"p-4 border-t {t['border']} {t['panel_bg']}")
            if isinstance(content, str): content_div <= html.P(content, Class=f"{t['text_muted']}")
            else: content_div <= content
            details <= summary
            details <= content_div
            container <= details
        return container

    @staticmethod
    def AccordionWithIcons(items, extra_class=""):
        t = UI.THEME
        container = html.DIV(Class=f"space-y-2 {extra_class}")
        for title, content, icon in items:
            details = html.DETAILS(Class="group [&_summary::-webkit-details-marker]:hidden")
            summary = html.SUMMARY(Class=f"flex cursor-pointer items-center justify-between gap-4 {t['radius']} border {t['border']} {t['panel_bg']} px-4 py-3 font-medium {t['text_main']} hover:{t['hover']}")
            header = html.SPAN(Class="flex items-center gap-2")
            header <= UI.Icon(icon, size=20, extra_class=t['text_muted'])
            header <= html.SPAN(title)
            summary <= header
            summary <= UI.Icon("M19 9l-7 7-7-7", size=20, extra_class=f"shrink-0 transition-transform duration-300 group-open:-rotate-180 {t['text_muted']}")
            
            content_div = html.DIV(Class=f"p-4 border-t {t['border']} {t['panel_bg']}")
            content_div <= html.P(str(content), Class=t['text_muted'])
            details <= summary
            details <= content_div
            container <= details
        return container

    @staticmethod
    def AccordionDivided(items, extra_class=""):
        t = UI.THEME
        divide = t['border'].replace('border-', 'divide-')
        container = html.DIV(Class=f"-mx-4 -my-2 space-y-0 divide-y {divide} {t['panel_bg']} border {t['border']} {t['radius']} {extra_class}")
        for title, content in items:
            details = html.DETAILS(Class="group px-4 py-3 [&_summary::-webkit-details-marker]:hidden")
            summary = html.SUMMARY(Class=f"flex cursor-pointer items-center justify-between gap-4 font-medium {t['text_main']} hover:text-{t['accent']}-400 transition-colors")
            summary <= html.SPAN(title)
            summary <= UI.Icon("M19 9l-7 7-7-7", size=20, extra_class=f"shrink-0 transition-transform duration-300 group-open:-rotate-180 {t['text_muted']}")
            content_div = html.DIV(Class="pt-4")
            content_div <= html.P(str(content), Class=t['text_muted'])
            details <= summary
            details <= content_div
            container <= details
        return container

    @staticmethod
    def AccordionNested(parent_items, extra_class=""):
        t = UI.THEME
        container = html.DIV(Class=f"space-y-2 {extra_class}")
        for p_title, children in parent_items:
            details = html.DETAILS(Class="group space-y-2 [&_summary::-webkit-details-marker]:hidden")
            summary = html.SUMMARY(Class=f"flex cursor-pointer items-center justify-between gap-4 {t['radius']} border {t['border']} {t['panel_bg']} px-4 py-3 font-medium {t['text_main']} hover:{t['hover']}")
            summary <= html.SPAN(p_title)
            summary <= UI.Icon("M19 9l-7 7-7-7", size=20, extra_class=f"shrink-0 transition-transform duration-300 group-open:-rotate-180 {t['text_muted']}")
            
            children_div = html.DIV(Class="space-y-2 pl-4")
            for c_title, c_desc in children:
                c_details = html.DETAILS(Class="group/child [&_summary::-webkit-details-marker]:hidden")
                c_summary = html.SUMMARY(Class=f"flex cursor-pointer items-center justify-between gap-4 {t['radius']} border {t['border']} bg-{t['accent']}-900/10 px-4 py-2 text-sm font-medium {t['text_main']} hover:bg-{t['accent']}-900/20")
                c_summary <= html.SPAN(c_title)
                c_summary <= UI.Icon("M19 9l-7 7-7-7", size=16, extra_class="shrink-0 transition-transform duration-300 group-open/child:-rotate-180 opacity-70")
                c_content = html.DIV(Class="p-4")
                c_content <= html.P(str(c_desc), Class=f"{t['text_muted']} text-sm")
                c_details <= c_summary
                c_details <= c_content
                children_div <= c_details
            
            details <= summary
            details <= children_div
            container <= details
        return container

    # ==========================================
    # 8. OVERLAYS (MODALES, TOASTS)
    # ==========================================

    @staticmethod
    def Modal(title, content, on_close=None, footer_actions=None, show_close_btn=True, size="md", extra_class=""):
        """
        Fenêtre modale (Popup).
        
        Args:
            title: Titre de la modale.
            content: Élément Brython (texte, formulaire...) ou str.
            on_close: Callback quand on ferme (croix ou clic extérieur).
            footer_actions: Liste de boutons [{'text': 'Cancel', 'onclick': cb}, {'text': 'Save', 'variant': 'primary'}].
            show_close_btn: Afficher la croix en haut à droite.
            size: "sm", "md", "lg", "xl".
        """
        t = UI.THEME
        
        # 1. Overlay (Fond sombre flouté)
        # animate-in fade-in pour l'effet d'apparition
        overlay = html.DIV(
            Class="fixed inset-0 z-50 grid place-content-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in",
            role="dialog",
            aria_modal="true"
        )
        
        # 2. Boîte de dialogue
        widths = {"sm": "max-w-sm", "md": "max-w-md", "lg": "max-w-lg", "xl": "max-w-xl"}
        box_width = widths.get(size, widths["md"])
        
        box = html.DIV(
            Class=f"w-full {box_width} rounded-lg {t['panel_bg']} border {t['border']} shadow-lg p-6 relative"
        )
        
        # 3. En-tête (Titre + Close Btn)
        header_cls = "flex items-start justify-between" if show_close_btn else ""
        header = html.DIV(Class=header_cls)
        
        # Titre H2
        header <= html.H2(title, Class=f"text-xl font-bold {t['text_main']} sm:text-2xl")
        
        # Bouton Close (X)
        if show_close_btn:
            close_btn = html.BUTTON(
                type="button",
                aria_label="Close",
                Class=f"-me-4 -mt-4 rounded-full p-2 {t['text_muted']} transition-colors hover:bg-white/10 hover:text-white focus:outline-none"
            )
            close_btn <= UI.Icon("M6 18L18 6M6 6l12 12", size=20) # w-5 h-5
            
            def _close_handler(ev):
                overlay.remove()
                if on_close: on_close()
                
            close_btn.bind("click", _close_handler)
            header <= close_btn
            
        box <= header
        
        # 4. Corps (Contenu)
        body = html.DIV(Class="mt-4")
        if isinstance(content, str):
            body <= html.P(content, Class=f"text-pretty {t['text_muted']}")
        else:
            body <= content
        box <= body
        
        # 5. Pied de page (Actions)
        if footer_actions:
            footer = html.FOOTER(Class="mt-6 flex justify-end gap-2")
            for action in footer_actions:
                variant = action.get("variant", "default")
                # Mapping variant -> classes boutons spécifiques aux modales (un peu plus soft)
                if variant == "primary":
                    btn_cls = f"rounded bg-{t['accent']}-600 px-4 py-2 text-sm font-medium text-white hover:bg-{t['accent']}-700"
                else: # default / secondary
                    btn_cls = f"rounded bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700"
                
                btn = html.BUTTON(action["text"], type="button", Class=btn_cls)
                
                # Gestion du clic : fermer la modale après l'action ?
                # On wrap le callback pour fermer sauf si auto_close=False
                def _action_click(ev, act=action):
                    if act.get("onclick"): act["onclick"](ev)
                    if act.get("auto_close", True): overlay.remove()
                    
                btn.bind("click", _action_click)
                footer <= btn
                
            box <= footer
            
        overlay <= box
        
        # Fermeture clic extérieur
        def _outside_click(ev):
            if ev.target == overlay:
                overlay.remove()
                if on_close: on_close()
        
        overlay.bind("click", _outside_click)
        
        # Injection dans le body (toujours au top)
        document.body <= overlay
        return overlay
    

    # ==========================================
    # 8. COMPOSANTS COMPLEXES : GROUPE DE BOUTONS
    # ==========================================

    @staticmethod
    def ButtonGroup(items, spacing="attached", size="md", variant="default", extra_class=""):
        """
        Groupe de boutons unifié (Base, Icons, Layouts).
        Traduction des composants "Button Group" de HyperUI.
        
        Args:
            items: Liste de dicts [{'text': 'Edit', 'icon': 'pencil', 'onclick': cb}, ...]
            spacing: "attached" (collés, style par défaut) ou "spaced" (écartés avec gap)
            size: "sm", "md", "lg"
            variant: "default" (gris/blanc) ou "primary" (couleur d'accent)
        """
        t = UI.THEME
        
        # 1. Configuration des tailles (Padding)
        sizes = {
            "sm": "px-2 py-1 text-xs",
            "md": "px-3 py-2 text-sm", # Correspond à l'exemple HyperUI
            "lg": "px-5 py-3 text-base"
        }
        pad_cls = sizes.get(size, sizes["md"])
        
        # 2. Configuration du conteneur
        # "attached" -> inline-flex simple
        # "spaced"   -> inline-flex gap-2 (Exemple "Layouts")
        container_cls = "inline-flex" if spacing == "attached" else "inline-flex gap-2"
        container = html.DIV(Class=f"{container_cls} {extra_class}")
        
        # 3. Construction des boutons
        for i, item in enumerate(items):
            text = item.get("text")
            icon = item.get("icon")
            onclick = item.get("onclick")
            active = item.get("active", False)
            
            # --- Gestion des Bordures et Arrondis ---
            # On extrait la taille du radius du thème (ex: 'rounded-md' -> 'md') pour construire rounded-s-md
            r_size = t['radius'].split('-')[-1] if '-' in t['radius'] else 'md'
            
            radius_cls = ""
            margin_cls = ""
            
            if spacing == "attached":
                # Style "Base" & "Icons"
                if i == 0: 
                    radius_cls = f"rounded-s-{r_size}" # Premier : arrondi gauche
                elif i == len(items) - 1: 
                    radius_cls = f"rounded-e-{r_size}" # Dernier : arrondi droite
                    margin_cls = "-ms-px" # Marge négative pour chevaucher la bordure
                else:
                    margin_cls = "-ms-px" # Milieu : pas d'arrondi, marge négative
            else:
                # Style "Layouts" (boutons séparés)
                radius_cls = t['radius'] # Tout le monde est arrondi
                
            # --- Styles de Base & Focus (Identique à HyperUI) ---
            # focus:z-10 est crucial pour que le focus ring passe au-dessus des voisins
            base_style = (
                f"{radius_cls} {margin_cls} border {pad_cls} font-medium transition-colors "
                f"focus:z-10 focus:ring-2 focus:ring-{t['accent']}-500 focus:outline-none"
            )
            
            # --- Gestion des Couleurs (Active vs Default) ---
            if active:
                # Style Actif (inspiré de HyperUI Main/Secondary)
                color_style = f"bg-{t['accent']}-600 text-white border-{t['accent']}-600 hover:bg-{t['accent']}-700"
            else:
                # Style Inactif (Dark mode friendly)
                # dark:border-gray-700 dark:text-gray-200 dark:hover:bg-gray-800
                color_style = (
                    f"{t['panel_bg']} border-{t['border'].replace('border-', '')} " # Hack propre pour récupérer la couleur de bordure
                    f"{t['text_main']} hover:bg-white/5 hover:text-white"
                )

            # Création du bouton
            btn = html.BUTTON(Class=f"{base_style} {color_style}")
            
            # Contenu (Flex si icône + texte)
            content_wrapper = html.DIV(Class="flex items-center gap-2")
            
            if icon:
                # size-5 correspond à 20px (w-5 h-5)
                content_wrapper <= UI.Icon(icon, size=20)
                
            if text:
                content_wrapper <= html.SPAN(text)
                
            btn <= content_wrapper
            
            if onclick:
                btn.bind("click", onclick)
                
            container <= btn
            
        return container

    # --- Raccourci pour groupe d'icônes uniquement ---
    @staticmethod
    def ButtonGroupIcons(icons, onclicks=None, **kwargs):
        """Helper pour créer rapidement le style 'Icons' de HyperUI."""
        items = []
        for idx, icon in enumerate(icons):
            cb = onclicks[idx] if onclicks and idx < len(onclicks) else None
            items.append({'icon': icon, 'onclick': cb})
        return UI.ButtonGroup(items, **kwargs)
    
    # ==========================================
    # 9. COMPOSANTS DE FORMULAIRE : CHECKBOXES
    # ==========================================

    @staticmethod
    def CheckboxGroup(items, variant="simple", name="checkbox-group", extra_class=""):
        """
        Groupe de cases à cocher (Checkboxes).
        
        Args:
            items: Liste de dictionnaires [{'id': 'opt1', 'label': 'Option 1', 'desc': 'Détail...', 'checked': True}, ...]
            variant: "simple" (label seul), "described" (avec description), "divided" (avec séparateurs)
            name: Attribut 'name' commun pour les inputs (utile pour les forms)
        """
        t = UI.THEME
        
        # Conteneur principal
        container_cls = "flex flex-col items-start gap-3"
        
        if variant == "divided":
            # Le style "Divided" nécessite un wrapper supplémentaire flow-root et divide-y
            # On transforme border-color en divide-color
            divide_color = t['border'].replace('border', 'divide')
            container_cls = f"-my-3 flex flex-col items-start divide-y {divide_color}"
            wrapper = html.DIV(Class="flow-root")
            inner_container = html.DIV(Class=f"{container_cls} {extra_class}")
            wrapper <= inner_container
            root = wrapper
            target_container = inner_container
        else:
            # Style standard (Simple / Described)
            root = html.FIELDSET(Class=extra_class)
            root <= html.LEGEND("Checkboxes", Class="sr-only") # Accessibilité
            container = html.DIV(Class=container_cls)
            root <= container
            target_container = container

        for item in items:
            item_id = item.get("id", f"chk-{name}-{item.get('label')}")
            label_text = item.get("label", "")
            description = item.get("desc", "")
            is_checked = item.get("checked", False)
            on_change = item.get("onchange", None)
            
            # --- Label Wrapper ---
            # Si "divided", on ajoute du padding vertical (py-3)
            label_cls = "inline-flex items-start gap-3 w-full cursor-pointer group" # w-full pour cliquer large
            if variant == "divided":
                label_cls += " py-3"
            
            label = html.LABEL(For=item_id, Class=label_cls)
            
            # --- Input Checkbox ---
            # Classes spécifiques pour tailwindcss/forms + Dark mode support
            # size-5 = w-5 h-5
            input_cls = (
                f"my-0.5 w-5 h-5 rounded border-gray-300 shadow-sm transition "
                f"text-{t['accent']}-600 focus:ring-{t['accent']}-500 " # Couleur de coche et ring
                f"dark:border-gray-600 dark:bg-gray-900 dark:ring-offset-gray-900 dark:checked:bg-{t['accent']}-600"
            )
            
            chk = html.INPUT(type="checkbox", Id=item_id, Name=name, Class=input_cls)
            if is_checked:
                chk.checked = True
            
            if on_change:
                chk.bind("change", lambda ev, cb=on_change, i=item: cb(ev, i))
            
            label <= chk
            
            # --- Contenu Texte (Titre + Description) ---
            text_wrapper = html.DIV()
            
            # Titre
            span_title = html.SPAN(label_text, Class=f"block font-medium {t['text_main']}")
            text_wrapper <= span_title
            
            # Description (si present)
            if description and variant in ["described", "divided"]:
                p_desc = html.P(description, Class=f"mt-0.5 text-sm {t['text_muted']}")
                text_wrapper <= p_desc
                
            label <= text_wrapper
            target_container <= label
            
        return root
    
    # ==========================================
    # 10. COMPOSANTS DE DONNÉES (LISTES)
    # ==========================================

    @staticmethod
    def DetailsList(items, variant="base", extra_class=""):
        """
        Liste de détails (Clé / Valeur) responsive.
        Traduction des "Details List" de HyperUI.
        
        Args:
            items: Liste de tuples (label, valeur) ou (label, valeur, is_html)
            variant: "base" (simple), "striped" (rayé), "bordered" (encadré), "striped-bordered"
            extra_class: Classes CSS additionnelles
        """
        t = UI.THEME
        
        # 1. Configuration du conteneur DL
        # Conversion de la couleur de bordure pour les séparateurs
        divide_cls = t['border'].replace('border-', 'divide-')
        
        # Classes de base pour la liste <dl>
        dl_classes = f"-my-3 divide-y {divide_cls} text-sm"
        
        # Gestion des styles Bordered
        if "bordered" in variant:
            dl_classes += f" rounded border {t['border']}"
            
        # Gestion des styles Striped (Couleur de fond alternée)
        # Note: On applique le style via CSS (child selector) pour la performance
        if "striped" in variant:
            # *:even:bg-gray-50 en Tailwind standard, ici adapté au dark mode
            # On utilise une couleur blanche très transparente pour marquer la ligne paire
            dl_classes += " *:even:bg-white/5"

        dl = html.DL(Class=dl_classes)
        
        # 2. Construction des lignes
        # Base: py-3 (padding vertical uniquement)
        # Striped/Bordered: p-3 (padding complet pour décoller des bords)
        padding_cls = "py-3" if variant == "base" else "p-3"
        
        for item in items:
            label = item[0]
            value = item[1]
            
            # Grille responsive : 1 colonne mobile, 3 colonnes desktop (Label 1 / Valeur 2)
            row = html.DIV(Class=f"grid grid-cols-1 gap-1 {padding_cls} sm:grid-cols-3 sm:gap-4")
            
            # Terme (Clé)
            dt = html.DT(label, Class=f"font-medium {t['text_main']}")
            
            # Description (Valeur)
            dd = html.DD(Class=f"{t['text_muted']} sm:col-span-2")
            
            # Gestion du contenu (Texte ou HTML)
            if isinstance(value, str):
                dd.text = value
            else:
                dd <= value
                
            row <= dt
            row <= dd
            dl <= row
            
        # Wrapper flow-root nécessaire pour gérer les marges négatives (-my-3) proprement
        wrapper = html.DIV(Class=f"flow-root {extra_class}")
        wrapper <= dl
        
        return wrapper
    
    # ==========================================
    # 11. COMPOSANTS DE SÉPARATION (DIVIDERS)
    # ==========================================

    @staticmethod
    def Divider(text=None, align="center", gradient=False, extra_class=""):
        """
        Séparateur horizontal avec ou sans texte.
        Traduction des "Dividers" de HyperUI.
        
        Args:
            text: Texte à afficher (optionnel)
            align: "center", "left", "right"
            gradient: True pour un effet fondu (transparent -> couleur)
            extra_class: Classes CSS (ex: "my-4" pour la marge)
        """
        t = UI.THEME
        
        # On dérive la couleur de fond de la ligne à partir de la couleur de bordure du thème
        # Ex: "border-slate-700" -> "bg-slate-700"
        line_color_cls = t['border'].replace("border-", "bg-")
        # Pour le gradient, on a besoin du nom de la couleur (ex: slate-700)
        color_name = line_color_cls.replace("bg-", "")
        
        container = html.SPAN(Class=f"flex items-center {extra_class}")
        
        # Helper pour créer une ligne
        def make_line(direction):
            if not gradient:
                # Ligne solide standard
                return html.SPAN(Class=f"h-px flex-1 {line_color_cls}")
            else:
                # Ligne dégradée (from-transparent to-color)
                # direction: "to-r" (gauche vers droite) ou "to-l" (droite vers gauche)
                grad_cls = f"bg-gradient-{direction}" # Note: j'utilise gradient (v3) au lieu de linear (v4) pour compatibilité max
                return html.SPAN(Class=f"h-px flex-1 {grad_cls} from-transparent to-{color_name}")

        # Logique d'assemblage selon l'alignement
        
        # 1. Ligne de Gauche
        if align in ["center", "right"]:
            # Si centre/droite, la ligne de gauche va vers la droite (to-r) pour toucher le texte
            container <= make_line("to-r")
            
        # 2. Texte (si présent)
        if text:
            # Gestion du padding selon l'alignement
            padding = "px-4"
            if align == "left": padding = "pe-4" # Padding End
            if align == "right": padding = "ps-4" # Padding Start
            
            container <= html.SPAN(text, Class=f"shrink-0 {padding} {t['text_main']}")
            
        # 3. Ligne de Droite
        if align in ["center", "left"]:
            # Si centre/gauche, la ligne de droite va vers la gauche (to-l) pour toucher le texte
            container <= make_line("to-l")
            
        return container
    
    # ==========================================
    # 12. COMPOSANTS DE NAVIGATION (DROPDOWNS)
    # ==========================================

    @staticmethod
    def Dropdown(trigger_text="Options", items=None, grouped=False, extra_class=""):
        """
        Menu déroulant (Dropdown).
        
        Args:
            trigger_text: Texte du bouton déclencheur.
            items: Liste d'items. 
                   Si grouped=False: [{'text': 'Edit', 'onclick': cb}, ...]
                   Si grouped=True: [{'title': 'General', 'items': [...]}, {'title': 'Actions', 'items': [...]}]
            grouped: True pour activer le mode sections (dividers).
        """
        t = UI.THEME
        
        # --- 1. Container Relative ---
        container = html.DIV(Class=f"relative inline-flex {extra_class}")
        
        # --- 2. Trigger (Bouton composé) ---
        # Le trigger est un 'inline-flex' avec le texte à gauche et la flèche à droite, séparés par une ligne
        trigger_wrapper = html.SPAN(
            Class=f"inline-flex divide-x {t['border'].replace('border-', 'divide-')} overflow-hidden "
                  f"{t['radius']} border {t['border']} {t['panel_bg']} shadow-sm"
        )
        
        # Partie Gauche (Texte)
        btn_main = html.BUTTON(
            trigger_text,
            type="button",
            Class=f"px-3 py-2 text-sm font-medium {t['text_main']} hover:{t['hover']} transition-colors focus:relative"
        )
        
        # Partie Droite (Flèche)
        btn_arrow = html.BUTTON(
            type="button",
            aria_label="Menu",
            Class=f"px-3 py-2 text-sm font-medium {t['text_main']} hover:{t['hover']} transition-colors focus:relative"
        )
        btn_arrow <= UI.Icon("M19.5 8.25l-7.5 7.5-7.5-7.5", size=16) # Chevron bas
        
        trigger_wrapper <= btn_main
        trigger_wrapper <= btn_arrow
        container <= trigger_wrapper
        
        # --- 3. Menu (Liste déroulante) ---
        # Par défaut caché (hidden), position absolute
        divide_cls = f"divide-y {t['border'].replace('border-', 'divide-')}" if grouped else ""
        
        menu = html.DIV(
            Class=f"absolute end-0 top-12 z-50 w-56 hidden "
                  f"{divide_cls} overflow-hidden {t['radius']} border {t['border']} {t['panel_bg']} shadow-lg",
            role="menu"
        )
        
        # Fonction pour générer un lien de menu
        def create_menu_item(item):
            label = item.get("text", "Item")
            onclick = item.get("onclick")
            is_danger = item.get("danger", False)
            
            if is_danger:
                cls = f"block w-full px-3 py-2 text-sm font-medium text-{t['danger']}-500 hover:bg-{t['danger']}-900/10 text-left"
            else:
                cls = f"block px-3 py-2 text-sm font-medium {t['text_main']} hover:{t['hover']} transition-colors"
                
            # On utilise BUTTON pour les actions, A pour les liens (ici BUTTON par défaut pour l'app)
            link = html.BUTTON(label, type="button", Class=cls, role="menuitem")
            if onclick: link.bind("click", onclick)
            return link

        # Construction du contenu du menu
        if grouped:
            # Mode Grouped : items est une liste de sections
            for section in items:
                group_div = html.DIV()
                # Titre de section optionnel (ex: "General")
                if section.get("title"):
                    group_div <= html.P(section["title"], Class=f"block px-3 py-2 text-xs font-bold uppercase {t['text_muted']}")
                
                # Items de la section
                for sub_item in section.get("items", []):
                    group_div <= create_menu_item(sub_item)
                menu <= group_div
        else:
            # Mode Simple : items est une liste plate
            for item in items:
                menu <= create_menu_item(item)

        container <= menu
        
        # --- 4. Interactivité (Toggle) ---
        def toggle_menu(ev):
            ev.stopPropagation()
            if "hidden" in menu.classList:
                # Fermer tous les autres dropdowns ouverts (optionnel mais recommandé)
                for open_menu in document.select('.dropdown-menu-open'):
                    open_menu.classList.add('hidden')
                    open_menu.classList.remove('dropdown-menu-open')
                
                menu.classList.remove("hidden")
                menu.classList.add("dropdown-menu-open") # Marqueur pour gérer la fermeture
            else:
                menu.classList.add("hidden")
                menu.classList.remove("dropdown-menu-open")

        # Le clic sur le bouton flèche OU le texte ouvre le menu
        btn_arrow.bind("click", toggle_menu)
        btn_main.bind("click", toggle_menu)
        
        # Fermeture au clic extérieur
        # Note: Ceci nécessite un gestionnaire global dans main.py, ou on l'attache au document ici
        # Pour une démo simple, on l'attache au document (attention aux fuites d'événements si bcp de dropdowns)
        def close_if_outside(ev):
            if not container.contains(ev.target):
                menu.classList.add("hidden")
                
        document.bind("click", close_if_outside)
        
        return container
    
    # ==========================================
    # 13. COMPOSANTS DE FEEDBACK (EMPTY STATES)
    # ==========================================

    @staticmethod
    def EmptyState(title, description, icon_path=None, action_content=None, extra_class=""):
        """
        État vide (Empty State) générique.
        
        Args:
            title: Titre principal (H2).
            description: Texte explicatif.
            icon_path: Path SVG de l'icône centrale (optionnel).
            action_content: Élément Brython à insérer sous le texte (Bouton, Liste, Input...).
            extra_class: Classes CSS additionnelles.
        """
        t = UI.THEME
        
        # Conteneur centré
        container = html.DIV(Class=f"max-w-md mx-auto text-center {extra_class}")
        
        # 1. Icône centrale (taille 20 = 80px)
        if icon_path:
            svg = html.SVG(
                html.PATH(d=icon_path, stroke_linecap="round", stroke_linejoin="round"),
                xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke_width="1.5", stroke="currentColor",
                Class=f"mx-auto w-20 h-20 {t['text_muted']}" # size-20 -> w-20 h-20
            )
            container <= svg
            
        # 2. Titre
        container <= html.H2(title, Class=f"mt-6 text-2xl font-bold {t['text_main']}")
        
        # 3. Description
        container <= html.P(description, Class=f"mt-4 text-pretty {t['text_muted']}")
        
        # 4. Zone d'action (si fournie)
        if action_content:
            wrapper = html.DIV(Class="mt-6")
            if isinstance(action_content, list):
                for item in action_content: wrapper <= item
            else:
                wrapper <= action_content
            container <= wrapper
            
        return container

    # --- Raccourcis pour les cas courants ---

    @staticmethod
    def EmptyStateCreate(title="No items found", desc="Get started by creating your first item.", on_create=None):
        """Cas 'Create first item'."""
        btn = UI.Button("Create Item", variant="primary", size="lg", onclick=on_create, extra_class="w-full justify-center")
        icon = "M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
        return UI.EmptyState(title, desc, icon, btn)

    @staticmethod
    def EmptyStateSearch(title="No results found", desc="Try adjusting your search or filters.", on_clear=None):
        """Cas 'No results found' (Recherche)."""
        t = UI.THEME
        
        # Action : Input search + Bouton clear
        wrapper = html.DIV(Class="space-y-2")
        inp = UI.Input(placeholder="Search again...")
        btn = UI.Button("Clear filters", variant="default", size="md", onclick=on_clear, extra_class="w-full justify-center")
        
        wrapper <= inp
        wrapper <= btn
        
        icon = "M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v16.5c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Zm3.75 11.625a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z"
        
        return UI.EmptyState(title, desc, icon, wrapper)
    

    # ==========================================
    # 14. COMPOSANTS DE FICHIERS (UPLOADER)
    # ==========================================

    @staticmethod
    def FileUploader(label="Upload your file(s)", with_button=False, multiple=True, on_change=None, extra_class=""):
        """
        Zone de téléchargement de fichiers (Drag & Drop).
        Traduction des composants "File Uploader" de HyperUI.
        
        Args:
            label: Texte principal.
            with_button: True pour afficher un bouton "Browse files" sous le texte.
            multiple: Autoriser plusieurs fichiers.
            on_change: Callback appelé quand des fichiers sont sélectionnés.
        """
        t = UI.THEME
        
        # Le conteneur est un LABEL qui pointe vers l'input caché
        # Cela rend toute la zone cliquable
        layout_cls = "flex flex-col items-center" if with_button else "flex items-center justify-center gap-4"
        
        container = html.LABEL(
            Class=f"block rounded border {t['border']} {t['panel_bg']} p-4 shadow-sm cursor-pointer "
                  f"hover:bg-white/5 transition-colors sm:p-6 {layout_cls} {extra_class}"
        )
        
        # Icône Upload (Nuage flèche)
        icon_path = "M7.5 7.5h-.75A2.25 2.25 0 0 0 4.5 9.75v7.5a2.25 2.25 0 0 0 2.25 2.25h7.5a2.25 2.25 0 0 0 2.25-2.25v-7.5a2.25 2.25 0 0 0-2.25-2.25h-.75m0-3-3-3m0 0-3 3m3-3v11.25m6-2.25h.75a2.25 2.25 0 0 1 2.25 2.25v7.5a2.25 2.25 0 0 1-2.25 2.25h-7.5a2.25 2.25 0 0 1-2.25-2.25v-.75"
        
        icon = UI.Icon(icon_path, size=24, extra_class=f"{t['text_main']}") # size-6 = 24px
        container <= icon
        
        # Texte Principal
        margin_cls = "mt-4" if with_button else ""
        text_span = html.SPAN(label, Class=f"{margin_cls} font-medium {t['text_main']}")
        container <= text_span
        
        # Bouton "Browse files" (optionnel, style visuel seulement)
        if with_button:
            browse_btn = html.SPAN(
                "Browse files",
                Class=f"mt-2 inline-block rounded border {t['border']} px-3 py-1.5 text-center text-xs font-medium "
                      f"{t['text_muted']} shadow-sm hover:text-white transition-colors"
            )
            container <= browse_btn
            
        # Input File Caché (sr-only)
        inp = html.INPUT(type="file", Class="sr-only")
        if multiple:
            inp.attrs["multiple"] = ""
            
        if on_change:
            inp.bind("change", on_change)
            
        container <= inp
        
        return container
    

    # ==========================================
    # 15. COMPOSANTS DE FILTRAGE
    # ==========================================

    @staticmethod
    def FilterGroup(label, content, variant="dropdown", count_text="0 Selected", on_reset=None, extra_class=""):
        """
        Composant de filtre riche (Dropdown ou Accordéon).
        
        Args:
            label: Titre du filtre (ex: "Price", "Availability").
            content: Élément Brython à afficher (Checkboxes, Inputs...).
            variant: "dropdown" (flottant absolute) ou "accordion" (expand in-place).
            count_text: Texte d'info en haut du panneau (ex: "Max price is $600").
            on_reset: Callback pour le bouton Reset.
        """
        t = UI.THEME
        
        # Élément principal : DETAILS
        details = html.DETAILS(Class=f"group relative {extra_class}")
        
        # --- 1. Résumé (Summary / Trigger) ---
        summary_cls = f"flex items-center gap-2 cursor-pointer text-sm font-medium {t['text_main']} [&::-webkit-details-marker]:hidden"
        
        if variant == "dropdown":
            # Style souligné pour dropdown
            summary_cls += f" border-b {t['border']} pb-1 transition-colors hover:text-{t['accent']}-400 hover:border-{t['accent']}-400"
        else:
            # Style bloc pour accordéon
            summary_cls += f" justify-between p-3 {t['panel_bg']} border {t['border']} {t['radius']} hover:{t['hover']}"

        summary = html.SUMMARY(Class=summary_cls)
        
        summary <= html.SPAN(label)
        
        # Icône chevron (rotative)
        svg = html.SVG(
            html.PATH(d="M19.5 8.25l-7.5 7.5-7.5-7.5", stroke_linecap="round", stroke_linejoin="round", stroke_width="1.5"),
            xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke="currentColor",
            Class="size-4 shrink-0 transition-transform group-open:-rotate-180"
        )
        summary <= svg
        details <= summary
        
        # --- 2. Panneau Déroulant ---
        panel_cls = f"z-50 w-64 {t['panel_bg']} border {t['border']} {t['radius']} shadow-sm"
        
        if variant == "dropdown":
            panel_cls += " absolute top-8 start-0" # Flottant
        else:
            panel_cls += " mt-1 border-t-0 rounded-t-none" # Collé dessous
            
        panel = html.DIV(Class=panel_cls)
        
        # En-tête du panneau (Compteur + Reset)
        header = html.DIV(Class=f"flex items-center justify-between px-3 py-2 border-b {t['border']}")
        header <= html.SPAN(count_text, Class=f"text-sm {t['text_muted']}")
        
        btn_reset = html.BUTTON(
            "Reset", 
            type="button",
            Class=f"text-sm underline transition-colors {t['text_muted']} hover:{t['text_main']}"
        )
        if on_reset:
            btn_reset.bind("click", on_reset)
        header <= btn_reset
        
        panel <= header
        
        # Contenu du filtre
        content_wrapper = html.DIV(Class="p-3")
        content_wrapper <= content
        panel <= content_wrapper
        
        details <= panel
        
        # Gestion fermeture clic extérieur (pour dropdown uniquement)
        if variant == "dropdown":
            def close_if_outside(ev):
                if not details.contains(ev.target):
                    details.removeAttribute("open")
            # Note: Pour une implémentation robuste, attacher ceci au document dans main.py
            # Ici on laisse le comportement natif de <details> qui est déjà pas mal
            pass 

        return details

    # --- Helper pour Inputs de Prix (Min/Max) ---
    @staticmethod
    def FilterPriceInputs(min_val=0, max_val=1000, currency="$"):
        """Génère la paire d'inputs Min/Max pour le filtre prix."""
        t = UI.THEME
        container = html.DIV(Class="flex items-center gap-3")
        
        def make_input(label, val):
            wrapper = html.LABEL(Class="flex flex-col gap-1")
            wrapper <= html.SPAN(label, Class=f"text-sm {t['text_muted']}")
            inp = html.INPUT(
                type="number", value=val, 
                Class=f"w-full rounded {t['input_bg']} border {t['border']} px-2 py-1 text-sm {t['text_main']} focus:border-{t['accent']}-500 focus:outline-none"
            )
            wrapper <= inp
            return wrapper
            
        container <= make_input("Min", min_val)
        container <= make_input("Max", max_val)
        return container
    
    # ==========================================
    # 16. COMPOSANTS DE LAYOUT (GRILLES)
    # ==========================================

    @staticmethod
    def Grid(items, cols=2, gap=4, extra_class=""):
        """
        Conteneur Grille Responsive (Grid System).
        Gère les layouts 1x1, 1x2, Sidebar, etc.
        
        Args:
            items: Liste des éléments à placer dans la grille.
            cols: Nombre de colonnes (int) OU définition personnalisée (str).
                  Ex: cols=3  -> 3 colonnes égales.
                  Ex: cols="120px_1fr" -> Sidebar gauche fixe + reste fluide.
            gap: Espace entre les éléments (défaut 4, double sur desktop).
        """
        # Construction de la classe de colonnes responsive
        # Mobile: toujours 1 colonne (grid-cols-1)
        # Desktop (lg): selon le paramètre cols
        if isinstance(cols, int):
            col_class = f"lg:grid-cols-{cols}"
        else:
            # Support des valeurs arbitraires Tailwind (ex: Sidebar layout)
            col_class = f"lg:grid-cols-[{cols}]"

        container = html.DIV(
            Class=f"grid grid-cols-1 gap-{gap} {col_class} lg:gap-{gap*2} {extra_class}"
        )
        
        for item in items:
            container <= item
            
        return container

    @staticmethod
    def GridItem(content, span=1, extra_class=""):
        """
        Élément de grille capable de s'étendre (Col Span).
        
        Args:
            content: Le contenu (Card, Panel, Text...).
            span: Nombre de colonnes à occuper (sur Desktop).
        """
        # lg:col-span-X s'active uniquement sur desktop
        span_cls = f"lg:col-span-{span}" if span > 1 else ""
        
        wrapper = html.DIV(Class=f"{span_cls} {extra_class}")
        
        # Si content est une liste, on ajoute les enfants, sinon l'élément direct
        if isinstance(content, list):
            for child in content: wrapper <= child
        else:
            wrapper <= content
            
        return wrapper
    
    # ==========================================
    # 17. COMPOSANTS DE CHARGEMENT (LOADERS)
    # ==========================================

    @staticmethod
    def Loader(text=None, inline=False, size="md", extra_class=""):
        """
        Spinner rotatif classique.
        Gère les styles : Base, With Message, Inline.
        
        Args:
            text: Texte à afficher (ex: "Loading...").
            inline: True pour mettre le texte à côté (layout horizontal).
            size: "sm" (24px), "md" (32px), "lg" (48px), "xl" (80px).
        """
        t = UI.THEME
        
        # Dimensions
        dim_map = {"sm": "w-6 h-6", "md": "w-8 h-8", "lg": "w-12 h-12", "xl": "w-20 h-20"}
        dim_cls = dim_map.get(size, dim_map["md"])
        
        # Conteneur
        if inline:
            container = html.DIV(Class=f"inline-flex items-center gap-3 {extra_class}")
        else:
            container = html.DIV(Class=f"text-center {extra_class}")
            
        # SVG Spinner
        svg = html.SVG(
            xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24",
            Class=f"animate-spin {dim_cls} text-{t['accent']}-600 dark:text-{t['accent']}-400 mx-auto"
        )
        
        # Cercle de fond (opacity-25)
        svg <= html.CIRCLE(cx="12", cy="12", r="10", stroke="currentColor", stroke_width="4", Class="opacity-25")
        
        # Chemin rotatif (opacity-75)
        path_d = "M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        svg <= html.PATH(d=path_d, fill="currentColor", Class="opacity-75")
        
        container <= svg
        
        # Texte (si présent)
        if text:
            # Si inline, pas de margin-top, sinon mt-4
            mt_cls = "" if inline else "mt-4"
            container <= html.P(text, Class=f"{mt_cls} font-medium {t['text_main']}")
            
        return container

    @staticmethod
    def LoaderBar(text=None, percentage="80%", extra_class=""):
        """
        Barre de chargement (Progress bar) avec animation.
        """
        t = UI.THEME
        
        container = html.DIV(Class=f"w-full max-w-sm mx-auto {extra_class}")
        
        # Barre de fond (gris)
        bg_bar = html.DIV(Class="h-2 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700")
        
        # Barre de progression (accent + pulse)
        # Note: on utilise style={"width": ...} pour la valeur dynamique
        progress = html.DIV(
            style={"width": percentage},
            Class=f"h-full animate-pulse bg-{t['accent']}-600 dark:bg-{t['accent']}-400"
        )
        bg_bar <= progress
        container <= bg_bar
        
        if text:
            container <= html.P(text, Class=f"mt-4 text-center font-medium {t['text_main']}")
            
        return container

    @staticmethod
    def LoaderDots(variant="pulse", extra_class=""):
        """
        Animation de 3 points.
        
        Args:
            variant: "pulse" (battement), "ping" (radar), "bounce" (rebond).
        """
        t = UI.THEME
        container = html.DIV(Class=f"flex gap-2 justify-center {extra_class}")
        
        # Mapping des animations Tailwind
        anim_map = {
            "pulse": "animate-pulse",
            "ping": "animate-ping",
            "bounce": "animate-bounce"
        }
        anim_cls = anim_map.get(variant, "animate-pulse")
        
        # Création des 3 points avec délai
        delays = ["", "animation-delay:0.2s", "animation-delay:0.4s"]
        
        for delay in delays:
            dot = html.SPAN(
                style={"animation-delay": "0.2s" if "0.2" in delay else "0.4s" if "0.4" in delay else "0s"},
                Class=f"w-3 h-3 rounded-full bg-{t['accent']}-600 dark:bg-{t['accent']}-400 {anim_cls}"
            )
            container <= dot
            
        return container
    

    # ==========================================
    # 18. COMPOSANTS MÉDIA (IMAGE + TEXTE)
    # ==========================================

    @staticmethod
    def MediaObject(title, description, image_src, align="start", reverse=False, size="md", extra_class=""):
        """
        Composant Média (Image + Texte).
        Gère les alignements (top, center, bottom, stretch) et la direction.
        
        Args:
            title: Titre principal.
            description: Texte descriptif.
            image_src: URL de l'image.
            align: "start" (haut), "center", "end" (bas), "stretch".
            reverse: True pour mettre l'image à droite.
            size: "sm" (16), "md" (20), "lg" (32).
        """
        t = UI.THEME
        
        # 1. Configuration Flexbox
        flex_dir = "flex-row-reverse" if reverse else ""
        align_cls = f"items-{align}"
        
        container = html.DIV(Class=f"flex {flex_dir} {align_cls} gap-4 {extra_class}")
        
        # 2. Image
        # Dimensions
        dim_map = {"sm": "w-16 h-16", "md": "w-20 h-20", "lg": "w-32 h-32"}
        # Si stretch, on ne fixe que la largeur, la hauteur s'adapte
        img_size_cls = f"w-{dim_map[size].split(' ')[0][2:]}" if align == "stretch" else f"size-{dim_map[size].split(' ')[0][2:]}" # size-20 ou w-20
        
        img = html.IMG(
            src=image_src,
            alt=title,
            Class=f"{img_size_cls} rounded object-cover bg-gray-200"
        )
        container <= img
        
        # 3. Contenu Texte
        # Si align=end ou reverse, le texte peut nécessiter un alignement spécifique (ici on garde standard gauche/droite)
        content_div = html.DIV()
        
        content_div <= html.H3(title, Class=f"font-medium {t['text_main']} sm:text-lg")
        content_div <= html.P(description, Class=f"mt-0.5 line-clamp-3 {t['text_muted']}")
        
        container <= content_div
        
        return container
    
    # ==========================================
    # 19. COMPOSANTS DE NAVIGATION (PAGINATION)
    # ==========================================

    @staticmethod
    def Pagination(current_page=1, total_pages=10, type="numbers", on_change=None, extra_class=""):
        """
        Barre de pagination.
        
        Args:
            current_page: Page actuelle (int).
            total_pages: Nombre total de pages.
            type: "numbers" (1 2 3...), "input" (Champ saisie), "fraction" (2/12).
            on_change: Callback appelé avec le nouveau numéro de page.
        """
        t = UI.THEME
        
        container = html.UL(Class=f"flex justify-center gap-1 {t['text_main']} {extra_class}")
        
        # --- Helper pour bouton Prev/Next ---
        def nav_btn(direction, icon_d):
            is_disabled = (direction == -1 and current_page <= 1) or (direction == 1 and current_page >= total_pages)
            
            btn_cls = f"grid size-8 place-content-center rounded border {t['border']} transition-colors rtl:rotate-180 "
            if is_disabled:
                btn_cls += "opacity-50 cursor-not-allowed"
            else:
                btn_cls += f"hover:{t['hover']}"
                
            li = html.LI()
            # On utilise BUTTON au lieu de A pour gérer l'event click plus proprement
            btn = html.BUTTON(type="button", Class=btn_cls, aria_label="Previous" if direction == -1 else "Next")
            
            svg = html.SVG(
                html.PATH(d=icon_d, fill_rule="evenodd", clip_rule="evenodd"),
                xmlns="http://www.w3.org/2000/svg", viewBox="0 0 20 20", fill="currentColor", Class="size-4"
            )
            btn <= svg
            
            if not is_disabled and on_change:
                btn.bind("click", lambda e: on_change(current_page + direction))
                
            li <= btn
            return li

        # Bouton Précédent
        container <= nav_btn(-1, "M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z")
        
        # --- Contenu Central (Variable selon le type) ---
        
        if type == "numbers":
            # Mode "1 2 3 4" (Simplifié: affiche current-1, current, current+1)
            # Pour une vraie pagination complexe, il faudrait plus de logique (ellipses...)
            # Ici on affiche une plage simple autour de la page courante
            start = max(1, current_page - 1)
            end = min(total_pages, current_page + 1)
            
            # Toujours afficher au moins la page 1 et la dernière si possible
            # (Pour la démo simple, on garde la logique HyperUI : quelques blocs)
            
            pages_to_show = range(start, end + 1)
            
            for p in pages_to_show:
                li = html.LI()
                if p == current_page:
                    # Page Active (Fond coloré)
                    link = html.SPAN(
                        str(p),
                        Class=f"block size-8 rounded border border-{t['accent']}-600 bg-{t['accent']}-600 text-center text-sm/8 font-medium text-white"
                    )
                else:
                    # Page Inactive
                    link = html.BUTTON(
                        str(p),
                        type="button",
                        Class=f"block size-8 rounded border {t['border']} text-center text-sm/8 font-medium transition-colors hover:{t['hover']}"
                    )
                    if on_change: link.bind("click", lambda e, pg=p: on_change(pg))
                    
                li <= link
                container <= li
                
        elif type == "input":
            # Mode Input (Saisie directe)
            li = html.LI()
            label = html.LABEL(For="PageNo", Class="sr-only")
            label.text = "Page"
            
            inp = html.INPUT(
                type="number", 
                value=current_page, 
                min=1, 
                max=total_pages,
                Class=f"h-8 w-16 rounded border {t['border']} {t['input_bg']} text-center text-sm focus:border-{t['accent']}-500 focus:outline-none"
            )
            
            # Trigger changement
            if on_change:
                def _handle_input(ev):
                    try:
                        val = int(ev.target.value)
                        if 1 <= val <= total_pages: on_change(val)
                    except: pass
                inp.bind("change", _handle_input)
                
            li <= label
            li <= inp
            container <= li
            
        elif type == "fraction":
            # Mode Fraction (2/12)
            li = html.LI(
                f"{current_page}/{total_pages}", 
                Class=f"text-sm/8 font-medium tracking-widest px-3"
            )
            container <= li

        # Bouton Suivant
        container <= nav_btn(1, "M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z")
        
        return container
    
    # ==========================================
    # 20. COMPOSANTS DE PROGRESSION (BARRES)
    # ==========================================

    @staticmethod
    def ProgressBar(value=0, max_val=100, label=None, show_value=True, meta=None, variant="default", size="md", extra_class=""):
        """
        Barre de progression linéaire.
        Gère les styles : Basic, With Labels, Compact.
        
        Args:
            value: Valeur actuelle.
            max_val: Valeur max (défaut 100).
            label: Titre à gauche (ex: "Updating").
            show_value: Afficher le pourcentage à droite (True/False).
            meta: Texte sous la barre (ex: "1.2 of 3.8 MB").
            variant: "default" (bleu), "success" (vert), "warning" (orange), "neutral" (gris).
            size: "sm" (fine, h-1), "md" (moyenne, h-2), "lg" (épaisse, h-4).
        """
        t = UI.THEME
        percentage = min(100, max(0, (value / max_val) * 100))
        
        container = html.DIV(
            role="progressbar",
            aria_valuenow=str(value),
            aria_valuemin="0",
            aria_valuemax=str(max_val),
            Class=f"{extra_class}"
        )
        
        # 1. En-tête (Label + Pourcentage)
        # Si label ou show_value, on crée un header flex
        if label or show_value:
            header = html.DIV(Class="flex justify-between gap-4 mb-2")
            
            if label:
                # Style compact (uppercase tracking-wide) si size="sm", sinon standard
                lbl_cls = f"text-xs font-medium tracking-wide {t['text_muted']} uppercase" if size == "sm" else f"text-sm font-medium {t['text_main']}"
                header <= html.SPAN(label, Class=lbl_cls)
                
            if show_value:
                val_text = f"{int(percentage)}%"
                header <= html.SPAN(val_text, Class=f"text-sm font-medium {t['text_main']}")
                
            container <= header
            
        # 2. La Barre (Track + Fill)
        # Hauteur selon size
        h_map = {"sm": "h-1", "md": "h-2", "lg": "h-4"}
        h_cls = h_map.get(size, "h-2")
        
        track = html.DIV(Class=f"{h_cls} w-full rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden")
        
        # Couleur selon variant
        color_map = {
            "default": f"bg-{t['accent']}-600",
            "success": "bg-emerald-600",
            "warning": "bg-amber-500",
            "neutral": "bg-gray-500"
        }
        bg_cls = color_map.get(variant, color_map["default"])
        
        fill = html.DIV(
            style={"width": f"{percentage}%"},
            Class=f"h-full rounded-full {bg_cls} transition-all duration-500"
        )
        
        track <= fill
        container <= track
        
        # 3. Métadonnées (Dessous)
        if meta:
            container <= html.P(meta, Class=f"mt-2 text-xs {t['text_muted']}")
            
        return container
    
    # ==========================================
    # 21. COMPOSANTS E-COMMERCE (QUANTITÉ)
    # ==========================================

    @staticmethod
    def QuantityInput(value=1, min_val=1, max_val=99, variant="base", centered=True, on_change=None, extra_class=""):
        """
        Sélecteur de quantité avec boutons +/-.
        
        Args:
            value: Valeur initiale.
            min_val: Minimum.
            max_val: Maximum.
            variant: "base" (boutons séparés), "bordered" (groupe unifié).
            centered: Centrer le texte dans l'input.
            on_change: Callback (valeur).
        """
        t = UI.THEME
        
        # Wrapper principal
        # Si bordered, on met la bordure sur le wrapper, sinon sur l'input
        wrapper_cls = "flex items-center"
        if variant == "bordered":
            wrapper_cls += f" rounded {t['border']} border"
        else:
            wrapper_cls += " gap-1"
            
        container = html.DIV(Class=f"{wrapper_cls} {extra_class}")
        
        # ID unique pour l'input
        inp_id = f"qty-{int(window.Math.random()*10000)}"
        
        # --- Input ---
        # Classes pour masquer les spinners natifs (Chrome/Firefox)
        no_spin_cls = "[-moz-appearance:textfield] [&::-webkit-inner-spin-button]:m-0 [&::-webkit-inner-spin-button]:appearance-none"
        text_align = "text-center" if centered else "text-left"
        
        # Style de l'input selon la variante
        if variant == "bordered":
            # Input transparent sans bordure (c'est le parent qui a la bordure)
            input_style = f"h-10 w-16 border-transparent {t['input_bg']} {t['text_main']} focus:ring-0"
        else:
            # Input standard avec sa propre bordure
            input_style = f"h-10 w-16 rounded border {t['border']} {t['input_bg']} {t['text_main']}"
            
        inp = html.INPUT(
            type="number", 
            Id=inp_id,
            value=value, 
            min=min_val, 
            max=max_val,
            Class=f"{input_style} {text_align} {no_spin_cls} sm:text-sm focus:outline-none"
        )

        # --- Boutons +/- ---
        def make_btn(label, delta):
            btn_cls = f"size-10 leading-10 {t['text_muted']} transition hover:opacity-75"
            btn = html.BUTTON(label, type="button", Class=btn_cls)
            
            def _click(ev):
                try:
                    curr = int(inp.value)
                    new_val = curr + delta
                    if min_val <= new_val <= max_val:
                        inp.value = new_val
                        if on_change: on_change(new_val)
                except: pass
                
            btn.bind("click", _click)
            return btn

        # Assemblage
        container <= html.LABEL("Quantity", For=inp_id, Class="sr-only") # Accessibilité
        container <= make_btn("−", -1)
        container <= inp
        container <= make_btn("+", 1)
        
        # Listener sur l'input direct
        if on_change:
            inp.bind("change", lambda e: on_change(int(e.target.value)))
            
        return container
    

    # ==========================================
    # 22. COMPOSANTS DE FORMULAIRE (RADIO)
    # ==========================================

    @staticmethod
    def RadioGroup(name, options, variant="card", on_change=None, extra_class=""):
        """
        Groupe de boutons radio.
        Gère les styles : Card (Bloc avec infos), Color (Cercles de couleur).
        
        Args:
            name: Nom du groupe (attribut name).
            options: Liste d'options.
                     Pour 'card': [{'id': 'opt1', 'label': 'Standard', 'meta': 'Free', 'checked': True}, ...]
                     Pour 'color': [{'id': 'red', 'color': 'red-500', 'checked': True}, ...]
            variant: "card", "card-input" (avec rond visible), "color".
            on_change: Callback (valeur sélectionnée).
        """
        t = UI.THEME
        
        # Conteneur Fieldset
        container = html.FIELDSET(Class=f"{extra_class}")
        container <= html.LEGEND(name, Class="sr-only") # Accessibilité
        
        # Layout Flex ou Space-y selon variant
        if variant == "color":
            layout_cls = "flex flex-wrap gap-3"
        else:
            layout_cls = "space-y-3"
            
        wrapper = html.DIV(Class=layout_cls)
        container <= wrapper
        
        for opt in options:
            opt_id = opt.get("id", f"{name}-{int(window.Math.random()*1000)}")
            val = opt.get("value", opt_id)
            is_checked = opt.get("checked", False)
            
            # --- Input Radio Caché (mais fonctionnel) ---
            # sr-only sauf si variant="card-input"
            input_cls = "size-5 border-gray-300 dark:border-gray-600 dark:bg-gray-900" if variant == "card-input" else "sr-only"
            
            inp = html.INPUT(type="radio", Name=name, Value=val, Id=opt_id, Class=input_cls)
            if is_checked: inp.checked = True
            
            if on_change:
                inp.bind("change", lambda e: on_change(e.target.value))
            
            # --- Label Wrapper ---
            
            if variant == "color":
                # Style Color Circle
                color_bg = f"bg-{opt.get('color', 'gray-500')}"
                # has-checked:ring-2 applique le ring quand l'input enfant est checked
                lbl_cls = (
                    f"block size-8 rounded-full {color_bg} shadow-sm cursor-pointer "
                    f"has-checked:ring-2 has-checked:ring-{opt.get('color', 'gray-500')} has-checked:ring-offset-2 dark:ring-offset-gray-900"
                )
                label = html.LABEL(For=opt_id, Class=lbl_cls)
                label <= inp
                label <= html.SPAN(opt_id, Class="sr-only") # Texte caché pour a11y
                
            else: # variant "card" ou "card-input"
                # Style Card (Bloc complet)
                lbl_cls = (
                    f"flex items-center justify-between gap-4 rounded border {t['border']} {t['panel_bg']} p-3 "
                    f"text-sm font-medium shadow-sm transition-colors cursor-pointer hover:{t['hover']} "
                    f"has-checked:border-{t['accent']}-600 has-checked:ring-1 has-checked:ring-{t['accent']}-600 " # Bordure active
                    f"dark:hover:bg-gray-800"
                )
                
                label = html.LABEL(For=opt_id, Class=lbl_cls)
                
                # Contenu Texte
                text_div = html.DIV() if variant == "card-input" else label
                
                # Titre
                text_div <= html.P(opt.get("label", ""), Class=f"{t['text_muted']} dark:text-gray-200")
                
                # Meta (Prix ou Info)
                if opt.get("meta"):
                    text_div <= html.P(opt.get("meta"), Class=f"{t['text_main']} dark:text-white")
                
                # Si input visible, on structure différemment
                if variant == "card-input":
                    label <= text_div
                    label <= inp
                else:
                    label <= inp # Input caché dedans
                    
            wrapper <= label
            
        return container
    
    # ==========================================
    # 23. COMPOSANTS DE FORMULAIRE (RANGE)
    # ==========================================

    @staticmethod
    def RangeSlider(label, min_val=0, max_val=100, value=50, step=1, show_output=False, min_max_labels=False, ticks=None, on_change=None, extra_class=""):
        """
        Curseur de sélection (Range Slider).
        
        Args:
            label: Texte du label.
            min_val, max_val, value, step: Paramètres numériques.
            show_output: Afficher la valeur actuelle à droite du slider.
            min_max_labels: Afficher "0%" et "100%" sous le slider.
            ticks: Liste de valeurs pour les graduations (ex: [0, 25, 50, 75, 100]). Active le style "Native".
            on_change: Callback (valeur).
        """
        t = UI.THEME
        
        # Container principal
        container = html.LABEL(Class=f"block {extra_class}")
        
        # Label Texte
        container <= html.SPAN(label, Class=f"block text-sm font-medium {t['text_main']}")
        
        # ID unique pour le datalist si besoin
        list_id = f"list-{int(window.Math.random()*10000)}" if ticks else None
        
        # --- Construction de l'Input ---
        
        # Si ticks est présent, on utilise le style natif (plus simple pour aligner les traits)
        # Sinon, on utilise le style Custom (Gros rond)
        is_custom = ticks is None
        
        if is_custom:
            # Classes CSS complexes pour styliser le "Thumb" (le rond qu'on tire)
            # On injecte la couleur d'accent du thème pour la bordure du rond
            thumb_style = (
                f"[&::-webkit-slider-thumb]:size-7 [&::-webkit-slider-thumb]:cursor-pointer "
                f"[&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:rounded-full "
                f"[&::-webkit-slider-thumb]:border-[6px] [&::-webkit-slider-thumb]:border-{t['accent']}-600 "
                f"[&::-webkit-slider-thumb]:bg-white dark:[&::-webkit-slider-thumb]:bg-gray-200"
            )
            
            # Fond de la barre (Track)
            track_style = "h-3.5 w-full appearance-none rounded-full bg-gray-300 dark:bg-gray-700"
            
            input_cls = f"mt-3 {track_style} {thumb_style}"
        else:
            # Style Natif pour les ticks
            input_cls = "mt-3 w-full cursor-pointer"

        inp = html.INPUT(
            type="range",
            min=min_val,
            max=max_val,
            value=value,
            step=step,
            Class=input_cls
        )
        
        if list_id:
            inp.attrs["list"] = list_id

        # --- Gestion de l'affichage (Output ou Simple) ---
        
        # Wrapper pour mettre l'output à côté si demandé
        wrapper = html.DIV(Class="flex items-center gap-3") if show_output else html.DIV()
        wrapper <= inp
        
        # Affichage de la valeur dynamique
        if show_output:
            output_span = html.SPAN(f"{value}", Class=f"text-sm font-medium {t['text_main']}")
            wrapper <= output_span
            
            # JS léger pour mettre à jour le texte en temps réel
            def update_output(ev):
                output_span.text = str(ev.target.value)
            inp.bind("input", update_output)

        container <= wrapper

        # --- Gestion des Ticks (Datalist) ---
        if ticks:
            datalist = html.DATALIST(Id=list_id, Class="flex w-full flex-col justify-between [writing-mode:vertical-lr]")
            for tick_val in ticks:
                datalist <= html.OPTION(value=tick_val, label=str(tick_val))
            container <= datalist

        # --- Gestion des Labels Min/Max (Dessous) ---
        if min_max_labels:
            labels_div = html.DIV(Class=f"mt-1 flex items-center justify-between text-xs font-medium {t['text_muted']}")
            labels_div <= html.SPAN(f"{min_val}")
            labels_div <= html.SPAN(f"{max_val}")
            container <= labels_div

        # --- Event Listener Global ---
        if on_change:
            inp.bind("change", lambda e: on_change(e.target.value))
            
        return container
    
        # ==========================================
    # 24. COMPOSANTS DE FORMULAIRE (SELECT)
    # ==========================================

    @staticmethod
    def Select(label, options, value=None, name=None, variant="base", placeholder="Please select", on_change=None, extra_class=""):
        """
        Menu déroulant (Select).
        
        Args:
            label: Texte du label.
            options: Liste d'options.
                     - Simple: [{'value': '1', 'text': 'One'}, ...] ou [('1', 'One'), ...]
                     - Groupes: [{'label': 'Group A', 'options': [...]}]
            value: Valeur sélectionnée par défaut.
            variant: "base" (Native select) ou "datalist" (Searchable input).
            placeholder: Texte par défaut (option vide ou placeholder input).
        """
        t = UI.THEME
        
        # ID unique pour lier label et input
        sel_id = f"sel-{int(window.Math.random()*10000)}"
        list_id = f"list-{sel_id}"
        
        container = html.LABEL(For=sel_id, Class=f"block {extra_class}")
        container <= html.SPAN(label, Class=f"text-sm font-medium {t['text_main']}")
        
        # Styles de base (Input/Select)
        # On utilise mt-1.5 pour un espacement propre
        base_cls = (
            f"mt-1.5 w-full rounded border {t['border']} {t['input_bg']} {t['text_main']} sm:text-sm shadow-sm "
            f"focus:ring-1 focus:ring-{t['accent']}-500 focus:border-{t['accent']}-500 focus:outline-none"
        )
        
        if variant == "datalist":
            # --- Mode DATALIST (Input avec recherche) ---
            wrapper = html.DIV(Class="relative")
            
            # Input
            # [&::-webkit-calendar-picker-indicator]:opacity-0 cache la flèche native moche de Chrome
            inp = html.INPUT(
                type="text", 
                Id=sel_id, 
                list=list_id, 
                placeholder=placeholder,
                value=value if value else "",
                Class=f"{base_cls} pe-8 [&::-webkit-calendar-picker-indicator]:opacity-0"
            )
            if on_change: inp.bind("change", on_change)
            wrapper <= inp
            
            # Flèche Custom (Icone Chevron)
            # pointer-events-none est crucial pour que le clic traverse vers l'input
            arrow = html.SPAN(Class=f"absolute inset-y-0 right-0 grid w-8 place-content-center {t['text_muted']} pointer-events-none")
            arrow <= UI.Icon("M19.5 8.25l-7.5 7.5-7.5-7.5", size=16)
            wrapper <= arrow
            
            container <= wrapper
            
            # Liste des options (Datalist cachée)
            datalist = html.DATALIST(Id=list_id)
            for opt in options:
                # Normalisation des options (dict, tuple ou valeur brute)
                val = opt.get('value') if isinstance(opt, dict) else opt[0] if isinstance(opt, tuple) else opt
                text = opt.get('text') if isinstance(opt, dict) else opt[1] if isinstance(opt, tuple) else opt
                datalist <= html.OPTION(value=val, label=str(text))
            container <= datalist
            
        else:
            # --- Mode BASE (Select natif) ---
            # Note: py-2 px-3 pour un padding confortable
            sel = html.SELECT(Id=sel_id, Name=name, Class=f"{base_cls} py-2 px-3")
            if on_change: sel.bind("change", on_change)
            
            # Option Placeholder
            if placeholder:
                sel <= html.OPTION(placeholder, value="")
                
            # Génération des options (supporte les groupes)
            for opt in options:
                if isinstance(opt, dict) and 'options' in opt:
                    # Cas : OPTGROUP
                    group = html.OPTGROUP(label=opt['label'], Class=f"text-{t['accent']}-600 font-bold")
                    for sub_opt in opt['options']:
                        val = sub_opt.get('value') if isinstance(sub_opt, dict) else sub_opt[0]
                        text = sub_opt.get('text') if isinstance(sub_opt, dict) else sub_opt[1]
                        o = html.OPTION(str(text), value=val, Class=f"{t['text_main']} font-normal")
                        if str(val) == str(value): o.selected = True
                        group <= o
                    sel <= group
                else:
                    # Cas : OPTION SIMPLE
                    if isinstance(opt, dict):
                        val, text = opt.get('value'), opt.get('text', opt.get('value'))
                    elif isinstance(opt, tuple) or isinstance(opt, list):
                        val, text = opt[0], opt[1]
                    else:
                        val, text = opt, opt
                        
                    o = html.OPTION(str(text), value=val)
                    if str(val) == str(value): o.selected = True
                    sel <= o
            
            container <= sel
            
        return container
    
    # ==========================================
    # 25. COMPOSANTS DE NAVIGATION (SIDE MENU)
    # ==========================================

    @staticmethod
    def SideMenu(items, brand=None, footer=None, collapsed=False, extra_class=""):
        """
        Menu latéral complet.
        
        Args:
            items: Liste de dicts définissant le menu.
                   Format item: {'label': 'Dashboard', 'icon': 'home', 'onclick': cb, 'active': True}
                   Format groupe: {'label': 'Teams', 'icon': 'users', 'subitems': [...]}
            brand: Élément (ou texte) pour le logo en haut.
            footer: Élément pour le bas (Profil, Logout...).
            collapsed: True pour le mode "Icon Only" (largeur 16).
        """
        t = UI.THEME
        
        width = "w-16" if collapsed else "w-64"
        
        # Conteneur principal (h-screen, sticky ou fixed selon besoin, ici flex container)
        container = html.DIV(
            Class=f"flex h-full flex-col justify-between border-e {t['border']} {t['panel_bg']} {width} transition-all duration-300 {extra_class}"
        )
        
        # --- Zone Haut (Logo + Nav) ---
        top_section = html.DIV(Class="px-4 py-6")
        
        # 1. Logo / Brand
        if brand:
            brand_wrapper = html.SPAN(
                Class=f"grid h-10 place-content-center rounded-lg {t['input_bg']} text-xs font-bold {t['text_muted']}"
            )
            if isinstance(brand, str):
                brand_wrapper.text = brand[:2].upper() if collapsed else brand
            else:
                brand_wrapper.clear()
                brand_wrapper <= brand
            top_section <= brand_wrapper

        # 2. Liste de Navigation
        nav_ul = html.UL(Class="mt-6 space-y-1")
        
        for item in items:
            nav_ul <= UI._SideMenuItem(item, collapsed)
            
        top_section <= nav_ul
        container <= top_section
        
        # --- Zone Bas (Sticky Footer) ---
        if footer:
            footer_div = html.DIV(Class=f"sticky inset-x-0 bottom-0 border-t {t['border']} p-2")
            footer_div <= footer
            container <= footer_div
            
        return container

    # --- Helper Interne pour les items du menu ---
    @staticmethod
    def _SideMenuItem(item, collapsed):
        t = UI.THEME
        label = item.get("label", "")
        icon = item.get("icon")
        onclick = item.get("onclick")
        active = item.get("active", False)
        subitems = item.get("subitems", [])
        
        # Styles de base
        base_cls = f"group relative flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-colors"
        
        if active:
            state_cls = f"bg-{t['accent']}-50 text-{t['accent']}-700 dark:bg-{t['accent']}-900/20 dark:text-{t['accent']}-100"
        else:
            state_cls = f"{t['text_muted']} hover:{t['hover']} hover:{t['text_main']}"
            
        # CAS 1: Mode Réduit (Icon Only)
        if collapsed:
            # En mode réduit, on n'affiche pas les sous-menus en accordéon (trop complexe UX), 
            # on traite tout comme des liens simples avec tooltip.
            li = html.LI()
            
            # Centrage spécifique pour mode icône
            link = html.A(href="#", Class=f"{base_cls} justify-center px-2")
            if onclick: link.bind("click", onclick)
            
            # Icône
            if icon: link <= UI.Icon(icon, size=20, extra_class="opacity-75")
            else: link <= html.SPAN(label[:1], Class="text-xs font-bold")
            
            # Tooltip (invisible -> visible on hover)
            tooltip = html.SPAN(
                label,
                Class=f"invisible absolute start-full top-1/2 ms-4 -translate-y-1/2 rounded bg-slate-900 px-2 py-1.5 text-xs font-medium text-white group-hover:visible z-50 whitespace-nowrap"
            )
            link <= tooltip
            
            li <= link
            return li

        # CAS 2: Mode Normal (Texte + Icone)
        
        # Sous-cas: Accordéon (Item avec sous-menus)
        if subitems:
            li = html.LI()
            details = html.DETAILS(Class="group [&_summary::-webkit-details-marker]:hidden")
            
            summary = html.SUMMARY(Class=f"flex cursor-pointer items-center justify-between {base_cls} {state_cls}")
            
            # Partie gauche (Icone + Label)
            left_div = html.DIV(Class="flex items-center gap-2")
            if icon: left_div <= UI.Icon(icon, size=20, extra_class="opacity-75")
            left_div <= html.SPAN(label)
            summary <= left_div
            
            # Chevron rotatif
            chevron = UI.Icon("M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z", size=16)
            chevron.classList.add("shrink-0", "transition", "duration-300", "group-open:-rotate-180")
            summary <= chevron
            
            details <= summary
            
            # Liste des sous-items
            ul_sub = html.UL(Class="mt-2 space-y-1 px-4")
            for sub in subitems:
                # Récursion pour les sous-items (toujours en mode non-collapsed ici)
                ul_sub <= UI._SideMenuItem(sub, False)
                
            details <= ul_sub
            li <= details
            return li
            
        # Sous-cas: Lien Simple
        else:
            li = html.LI()
            link = html.A(href="#", Class=f"{base_cls} {state_cls}")
            if onclick: link.bind("click", onclick)
            
            if icon: link <= UI.Icon(icon, size=20, extra_class="opacity-75")
            link <= html.SPAN(label)
            
            li <= link
            return li

    @staticmethod
    def SideMenuProfile(name, email, avatar_url=None, extra_class=""):
        """Composant Profil pour le footer du menu."""
        t = UI.THEME
        
        container = html.A(href="#", Class=f"flex items-center gap-2 rounded-lg p-2 hover:{t['hover']} {extra_class}")
        
        # Avatar
        if avatar_url:
            img = html.IMG(src=avatar_url, alt=name, Class="size-10 rounded-full object-cover")
            container <= img
        else:
            # Fallback avatar
            placeholder = html.DIV(
                Class=f"grid size-10 place-content-center rounded-full bg-{t['accent']}-100 text-{t['accent']}-600 font-bold"
            )
            placeholder.text = name[:2].upper()
            container <= placeholder
            
        # Info
        info_div = html.DIV()
        info_div <= html.P(html.STRONG(name, Class="block font-medium"), Class=f"text-xs {t['text_main']}")
        info_div <= html.SPAN(email, Class=f"text-xs {t['text_muted']}")
        container <= info_div
        
        return container
    
    # ==========================================
    # 26. COMPOSANTS D'ACCESSIBILITÉ (SKIP LINKS)
    # ==========================================

    @staticmethod
    def SkipLinks(links, title="Skip to:", variant="simple", extra_class=""):
        """
        Liens d'évitement (invisibles sauf au focus clavier).
        Essentiel pour l'accessibilité (A11y).
        
        Args:
            links: Liste de tuples [('Label', '#anchor')] ou tuple unique ('Label', '#anchor').
            title: Titre pour le mode "panel" (ex: "Naviguer vers :").
            variant: "simple" (Bouton central), "panel" (Barre complète).
        """
        t = UI.THEME
        
        # Normalisation : si un seul tuple est passé, on le met dans une liste
        if isinstance(links, tuple):
            links = [links]
            
        # --- CAS 1: Simple (Bouton unique centré) ---
        if variant == "simple":
            # On prend le premier lien
            label, anchor = links[0]
            
            # Position: centré horizontalement, caché en haut (-translate-y-full)
            # Au focus: descend (translate-y-4)
            return html.A(
                label,
                href=anchor,
                Class=f"fixed top-0 left-1/2 -translate-x-1/2 -translate-y-full z-[100] "
                      f"rounded bg-{t['accent']}-600 px-6 py-3 text-sm font-bold text-white shadow-lg "
                      f"transition-transform focus:translate-y-4 focus:outline-none focus:ring-2 focus:ring-white"
            )

        # --- CAS 2: Panel (Barre avec plusieurs liens) ---
        elif variant == "panel":
            # Container NAV
            # focus-within permet d'afficher la nav si N'IMPORTE QUEL lien dedans a le focus
            nav = html.NAV(
                Class=f"fixed inset-x-0 top-0 z-[100] flex -translate-y-full items-center gap-3 "
                      f"{t['panel_bg']} border-b {t['border']} p-4 shadow-md "
                      f"transition-transform focus-within:translate-y-0",
                aria_label="Skip links"
            )
            
            # Titre
            if title:
                nav <= html.P(
                    title, 
                    Class=f"text-xs font-bold tracking-wide {t['text_muted']} uppercase"
                )
                
            # Liens
            wrapper = html.DIV(Class="flex flex-wrap gap-2")
            for label, anchor in links:
                link = html.A(
                    label,
                    href=anchor,
                    Class=f"text-sm font-medium {t['accent_text']} underline decoration-2 underline-offset-2 "
                          f"hover:{t['text_main']} transition-colors outline-none focus:text-{t['accent']}-500"
                )
                wrapper <= link
                
            nav <= wrapper
            return nav
        
    # ==========================================
    # 27. COMPOSANTS DE DONNÉES (STATS)
    # ==========================================

    @staticmethod
    def StatCard(label, value, growth=None, growth_label="Since last week", icon=None, stacked=False, extra_class=""):
        """
        Carte de statistique (KPI).
        
        Args:
            label: Titre (ex: "Profit").
            value: Valeur principale (ex: "$404.32").
            growth: Pourcentage de croissance (float, ex: 67.81 ou -12.5).
            growth_label: Texte explicatif de la croissance.
            icon: Nom de l'icône ou path SVG (optionnel).
            stacked: Si True, affiche la croissance en dessous (style compact).
        """
        t = UI.THEME
        
        container = html.ARTICLE(
            Class=f"rounded-lg border {t['border']} {t['panel_bg']} p-6 {extra_class}"
        )
        
        # --- Helper pour le Badge Croissance ---
        growth_badge = None
        if growth is not None:
            is_positive = growth >= 0
            color = "green" if is_positive else "red"
            icon_d = "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" if is_positive else "M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"
            
            # Badge
            badge_cls = f"inline-flex gap-2 rounded-sm bg-{color}-100 p-1 text-{color}-600 dark:bg-{color}-700 dark:text-{color}-50"
            growth_badge = html.DIV(Class=badge_cls)
            
            svg = html.SVG(
                html.PATH(d=icon_d, stroke_linecap="round", stroke_linejoin="round", stroke_width="2"),
                xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke="currentColor", Class="size-4"
            )
            growth_badge <= svg
            growth_badge <= html.SPAN(f"{abs(growth)}%", Class="text-xs font-medium")

        # --- Layout ---
        
        # Partie Contenu (Titre + Valeur)
        content_div = html.DIV()
        
        # Si layout standard (non stacked), on utilise flex pour séparer contenu et badge/icon
        wrapper_cls = "flex items-center justify-between" if not stacked else ""
        wrapper = html.DIV(Class=wrapper_cls)
        
        # Bloc infos
        info_block = html.DIV()
        info_block <= html.P(label, Class=f"text-sm font-medium {t['text_muted']}")
        info_block <= html.P(value, Class=f"text-2xl font-medium {t['text_main']}")
        
        # Gestion de l'icône principale
        if icon:
            icon_span = html.SPAN(Class=f"rounded-full bg-{t['accent']}-100 p-3 text-{t['accent']}-600 dark:bg-{t['accent']}-500/20 dark:text-{t['accent']}-400")
            icon_span <= UI.Icon(icon, size=32) # size-8
            
            # Si icône présente, on l'affiche à gauche ou droite selon le design
            # Ici on reproduit le style "Title, value and icon" : icône à gauche, texte à droite
            # Ou "stacked" : icône à droite
            inner_flex = html.DIV(Class="flex items-center gap-4")
            if stacked: # Icone à droite dans le header
                wrapper.classList.add("items-center") # Force l'alignement
                wrapper <= info_block
                wrapper <= icon_span
                container <= wrapper
            else: # Icone à gauche
                inner_flex <= icon_span
                inner_flex <= info_block
                wrapper <= inner_flex
                # Si growth présent en mode non-stacked, on le met à droite
                if growth_badge: wrapper <= growth_badge
                container <= wrapper
        else:
            # Pas d'icône
            wrapper <= info_block
            if growth_badge and not stacked: wrapper <= growth_badge
            container <= wrapper

        # --- Partie Growth (si Stacked) ---
        if stacked and growth_badge:
            footer = html.DIV(Class=f"mt-1 flex gap-1 text-{color}-600")
            footer <= growth_badge # On réutilise le badge créé
            # Le badge contient déjà l'icône et le %, on ajoute le texte explicatif à côté ?
            # HyperUI met tout dans le même bloc texte. Adaptons :
            
            # Reconstruction pour correspondre exactement au style stacked HyperUI
            # (SVG + Pourcentage + Texte gris)
            stacked_footer = html.DIV(Class=f"mt-4 flex gap-2 text-{color}-600 items-center")
            
            # On reprend juste le SVG du badge
            svg_clone = growth_badge.children[0] 
            stacked_footer <= svg_clone
            
            p_text = html.P(Class="flex gap-2 text-xs")
            p_text <= html.SPAN(f"{abs(growth)}%", Class="font-medium")
            p_text <= html.SPAN(growth_label, Class=f"{t['text_muted']}")
            stacked_footer <= p_text
            
            container <= stacked_footer

        return container

    # ==========================================
    # 28. COMPOSANTS DE NAVIGATION (STEPS)
    # ==========================================

    @staticmethod
    def Steps(steps, current_step=1, variant="simple", extra_class=""):
        """
        Indicateur d'étapes (Wizard).
        
        Args:
            steps: Liste de titres ou dicts [{'label': 'Address', 'icon': 'home'}].
            current_step: Index de l'étape active (1-based).
            variant: "simple" (Icon+Bar), "fraction" (2/3), "timeline" (Numéros), "grouped" (Blocs fléchés).
        """
        t = UI.THEME
        total = len(steps)
        
        # --- Variant: Fraction (Minimaliste) ---
        if variant == "fraction":
            # Juste "2/3 - Label" et une barre
            active_label = steps[current_step-1] if isinstance(steps[current_step-1], str) else steps[current_step-1].get('label')
            
            container = html.DIV(Class=extra_class)
            container <= html.H2("Steps", Class="sr-only")
            
            container <= html.P(f"{current_step}/{total} - {active_label}", Class=f"text-xs font-medium {t['text_muted']}")
            
            # Barre de progression
            bg_bar = html.DIV(Class="mt-2 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700")
            progress = html.DIV(
                style={"width": f"{(current_step/total)*100}%"},
                Class=f"h-2 rounded-full bg-{t['accent']}-600"
            )
            bg_bar <= progress
            container <= bg_bar
            return container

        # --- Variants Liste (Simple, Timeline, Grouped) ---
        
        container = html.DIV(Class=extra_class)
        container <= html.H2("Steps", Class="sr-only")
        
        # Structure de base
        if variant == "timeline":
            # Barre de fond traversante
            ol_wrapper = html.DIV(Class="relative after:absolute after:inset-x-0 after:top-1/2 after:block after:h-0.5 after:-translate-y-1/2 after:rounded-lg after:bg-gray-200 dark:after:bg-gray-700")
            ol = html.OL(Class="relative z-10 flex justify-between text-sm font-medium text-gray-600 dark:text-gray-300")
            ol_wrapper <= ol
            container <= ol_wrapper
        elif variant == "grouped":
            ol = html.OL(
                Class=f"grid grid-cols-1 divide-x {t['border'].replace('border-', 'divide-')} overflow-hidden rounded-lg border {t['border']} text-sm text-gray-600 dark:text-gray-300 sm:grid-cols-{total}"
            )
            container <= ol
        else: # simple
            # Barre de progression globale en haut
            bar_div = html.DIV(Class="overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700")
            bar_fill = html.DIV(
                style={"width": f"{(current_step/total)*100}%"},
                Class=f"h-2 rounded-full bg-{t['accent']}-600"
            )
            bar_div <= bar_fill
            container <= bar_div
            
            ol = html.OL(Class=f"mt-4 grid grid-cols-{total} text-sm font-medium text-gray-600 dark:text-gray-300")
            container <= ol

        # Génération des items
        for i, step_data in enumerate(steps):
            step_idx = i + 1
            label = step_data if isinstance(step_data, str) else step_data.get('label')
            # Icône par défaut si non fournie (pour le mode simple)
            icon = step_data.get('icon', 'check') if isinstance(step_data, dict) else 'check'
            
            # États
            is_completed = step_idx < current_step
            is_current = step_idx == current_step
            
            color_cls = f"text-{t['accent']}-600 dark:text-{t['accent']}-400" if (is_completed or is_current) else ""
            
            # --- Item pour Timeline ---
            if variant == "timeline":
                li = html.LI(Class=f"flex items-center gap-2 {t['panel_bg']} p-2")
                
                # Rond Numéro
                if is_current:
                    num_cls = f"bg-{t['accent']}-600 text-white"
                elif is_completed:
                    num_cls = f"bg-{t['accent']}-600 text-white" # Ou vert pour completed ? HyperUI met bleu
                else:
                    num_cls = "bg-gray-100 dark:bg-gray-800"
                    
                li <= html.SPAN(str(step_idx), Class=f"size-6 rounded-full text-center text-[10px]/6 font-bold {num_cls}")
                li <= html.SPAN(label, Class="hidden sm:block")
                ol <= li
                
            # --- Item pour Grouped (Flèches) ---
            elif variant == "grouped":
                # Le style est complexe avec des pseudo-éléments pour les flèches, simplifions pour Brython
                # On utilise simplement un fond coloré pour l'actif
                bg_cls = f"bg-gray-50 dark:bg-gray-800" if is_current else ""
                li = html.LI(Class=f"flex items-center justify-center gap-2 p-4 {bg_cls}")
                
                # Icône
                li <= UI.Icon(icon, size=24) # size-7
                
                text_div = html.P(Class="leading-none")
                text_div <= html.STRONG(label, Class=f"block font-medium {t['text_main']}")
                text_div <= html.SMALL("Description...", Class="mt-1") # Placeholder description
                li <= text_div
                ol <= li
                
            # --- Item pour Simple (Icon + Text) ---
            else:
                # Alignement (Gauche pour 1er, Droite pour dernier, Centre pour autres)
                align = "justify-start" if i == 0 else "justify-end" if i == total - 1 else "justify-center"
                
                li = html.LI(Class=f"flex items-center {align} {color_cls} sm:gap-1.5")
                
                li <= html.SPAN(label, Class="hidden sm:inline")
                # Icône svg
                li <= UI.Icon(icon, size=24) # size-6
                
                ol <= li
                
        return container

    # ==========================================
    # 29. COMPOSANTS DE DONNÉES (TABLES)
    # ==========================================

    @staticmethod
    def Table(columns, data, variant="base", extra_class=""):
        """
        Tableau de données responsive.
        
        Args:
            columns: Liste de titres de colonnes ["Name", "Role"...] ou dicts.
            data: Liste de listes (lignes) ou liste de dicts (si clés match colonnes).
            variant: Combinaison de "bordered", "striped", "sticky-header", "sticky-col".
        """
        t = UI.THEME
        
        # Wrapper Overflow (Scroller horizontal)
        # Si sticky-header, on limite la hauteur (max-h-64 par ex)
        wrapper_cls = "overflow-x-auto"
        if "sticky-header" in variant: wrapper_cls += " max-h-96" # Hauteur fixe pour que le sticky fonctionne
        if "bordered" in variant: wrapper_cls += f" rounded border {t['border']} shadow-sm"
        
        wrapper = html.DIV(Class=f"{wrapper_cls} {extra_class}")
        
        # Table
        # divide-y pour séparer les lignes
        table_cls = f"min-w-full divide-y-2 {t['border'].replace('border-', 'divide-')} text-sm"
        table = html.TABLE(Class=table_cls)
        
        # --- THEAD ---
        # Classes de l'en-tête
        thead_cls = "ltr:text-left rtl:text-right"
        if "sticky-header" in variant:
            thead_cls += f" sticky top-0 {t['panel_bg']} z-10" # z-10 pour passer au dessus du body
            
        thead = html.THEAD(Class=thead_cls)
        tr_head = html.TR(Class=f"*:font-medium {t['text_main']}")
        
        for idx, col in enumerate(columns):
            label = col if isinstance(col, str) else col.get("label", str(col))
            th_cls = "px-4 py-2 whitespace-nowrap"
            
            # Gestion Sticky First Column (Header)
            if idx == 0 and "sticky-col" in variant:
                th_cls += f" sticky left-0 {t['panel_bg']} z-20" # z-20 pour passer au dessus des autres TH
                
            tr_head <= html.TH(label, Class=th_cls)
            
        thead <= tr_head
        table <= thead
        
        # --- TBODY ---
        # Classes du corps
        tbody_cls = f"divide-y {t['border'].replace('border-', 'divide-')}"
        if "striped" in variant:
            tbody_cls += " *:even:bg-gray-50 dark:*:even:bg-gray-800/50" # Zébrure
            
        tbody = html.TBODY(Class=tbody_cls)
        
        for row in data:
            tr = html.TR(Class=f"*:text-{t['text_main']} {t['hover']}")
            
            # Normalisation des données de ligne (list ou dict)
            # Si dict, on assume que l'ordre des valeurs suit l'ordre des colonnes (simplification)
            # ou on prend values()
            cells = row.values() if isinstance(row, dict) else row
            
            for idx, cell in enumerate(cells):
                td_cls = "px-4 py-2 whitespace-nowrap"
                
                # Gestion Sticky First Column (Body)
                if idx == 0:
                    td_cls += " font-medium" # Première colonne en gras souvent
                    if "sticky-col" in variant:
                        td_cls += f" sticky left-0 {t['panel_bg']}"
                else:
                    td_cls += f" {t['text_muted']}"
                    
                tr <= html.TD(str(cell), Class=td_cls)
                
            tbody <= tr
            
        table <= tbody
        wrapper <= table
        return wrapper

    # ==========================================
    # 30. COMPOSANTS DE NAVIGATION (TABS)
    # ==========================================

    @staticmethod
    def Tabs(tabs_data, variant="underline", vertical=False, extra_class=""):
        """
        Système d'onglets complet.
        
        Args:
            tabs_data: Liste de dictionnaires [{'label': 'Tab 1', 'content': element, 'icon': 'user'}, ...]
            variant: "underline" (bordure bas), "pills" (boutons pleins), "lifted" (style dossier).
            vertical: Si True, affiche les onglets à gauche (layout flex row).
        """
        t = UI.THEME
        
        # ID unique pour ce groupe d'onglets
        group_id = f"tabs-{int(window.Math.random()*10000)}"
        
        # Conteneur principal
        # Si vertical, on utilise flex-row, sinon flex-col (par défaut div est block)
        container_cls = "flex gap-4" if vertical else f"{extra_class}"
        container = html.DIV(Class=container_cls)
        
        # --- 1. Liste des Onglets (TabList) ---
        
        # Styles du conteneur de liste
        if vertical:
            list_cls = f"flex flex-col gap-1 border-r {t['border']} min-w-[150px]"
        elif variant == "pills":
            list_cls = "flex gap-2"
        else: # underline (default)
            list_cls = f"flex gap-4 border-b {t['border']}"
            
        tablist = html.DIV(role="tablist", Class=list_cls)
        
        # --- 2. Panneaux de Contenu (TabPanels) ---
        panels_container = html.DIV(Class="flex-1 mt-4" if not vertical else "flex-1")
        
        # Stockage des références pour la logique de switch
        tab_buttons = []
        tab_panels = []
        
        for i, tab in enumerate(tabs_data):
            tab_id = f"{group_id}-tab-{i}"
            panel_id = f"{group_id}-panel-{i}"
            label = tab.get("label", f"Tab {i+1}")
            icon = tab.get("icon")
            content = tab.get("content", "No content")
            is_active = i == 0
            
            # --- Création du Bouton ---
            # Styles de base
            btn_base = "group flex items-center gap-2 text-sm font-medium transition-colors focus:outline-none whitespace-nowrap"
            
            # Styles Actif vs Inactif selon variant
            if variant == "pills":
                # Style Pills
                active_cls = f"rounded-full bg-{t['accent']}-600 text-white"
                inactive_cls = f"rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
                style_cls = f"{btn_base} px-4 py-2 {active_cls if is_active else inactive_cls}"
                
            else: # underline ou vertical
                # Style Underline / Vertical Border
                # On gère la border-b (horizontal) ou border-r (vertical)
                border_side = "border-r-2" if vertical else "border-b-2"
                
                # Note: -mb-px ou -mr-px pour chevaucher la ligne du conteneur
                margin_fix = "-mr-px" if vertical else "-mb-px"
                
                active_cls = f"border-{t['accent']}-600 text-{t['accent']}-600"
                inactive_cls = f"border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-200"
                
                style_cls = f"{btn_base} {margin_fix} {border_side} px-4 py-2 {active_cls if is_active else inactive_cls}"

            btn = html.BUTTON(
                role="tab",
                aria_selected=str(is_active).lower(),
                aria_controls=panel_id,
                Id=tab_id,
                Class=style_cls
            )
            
            if icon:
                btn <= UI.Icon(icon, size=16)
            btn <= html.SPAN(label)
            
            tablist <= btn
            tab_buttons.append(btn)
            
            # --- Création du Panneau ---
            panel = html.DIV(
                role="tabpanel",
                Id=panel_id,
                aria_labelledby=tab_id,
                Class="block" if is_active else "hidden"
            )
            
            if isinstance(content, str):
                panel <= html.P(content, Class=f"{t['text_muted']}")
            else:
                panel <= content
                
            panels_container <= panel
            tab_panels.append(panel)

        # --- 3. Logique de Switch (Interne) ---
        def switch_tab(idx):
            for i, (b, p) in enumerate(zip(tab_buttons, tab_panels)):
                is_selected = i == idx
                
                # Mise à jour ARIA
                b.attrs["aria-selected"] = str(is_selected).lower()
                
                # Mise à jour Visibilité Panneau
                if is_selected:
                    p.classList.remove("hidden")
                    p.classList.add("block")
                else:
                    p.classList.remove("block")
                    p.classList.add("hidden")
                
                # Mise à jour Styles Bouton (Le plus dur en CSS utility-first sans frameworks JS)
                # On doit échanger les classes active/inactive
                # Simplification: On recalcule les classes complètes ou on toggle
                
                # Pour faire simple et robuste en Brython :
                # On retire TOUTES les classes de couleur/border spécifiques et on remet les bonnes
                # Mais c'est lourd. 
                # Astuce : Utiliser une classe marqueur "active-tab" et laisser le CSS gérer ? Non, Tailwind pur.
                
                # Méthode brute : Recréer les strings de classes (comme à l'init)
                # C'est un peu verbeux mais sûr.
                
                if variant == "pills":
                    ac = f"bg-{t['accent']}-600 text-white"
                    ic = "bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
                    # On nettoie les anciennes (on assume qu'elles sont là)
                    # Plus simple: on reset le className complet basé sur l'index
                    base = "group flex items-center gap-2 text-sm font-medium transition-colors focus:outline-none whitespace-nowrap px-4 py-2 rounded-full"
                    b.className = f"{base} {ac if is_selected else ic}"
                    
                else: # underline
                    border_s = "border-r-2" if vertical else "border-b-2"
                    m_fix = "-mr-px" if vertical else "-mb-px"
                    ac = f"border-{t['accent']}-600 text-{t['accent']}-600"
                    ic = "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-200"
                    base = f"group flex items-center gap-2 text-sm font-medium transition-colors focus:outline-none whitespace-nowrap px-4 py-2 {border_s} {m_fix}"
                    b.className = f"{base} {ac if is_selected else ic}"

        # Attachement des events
        for i, btn in enumerate(tab_buttons):
            # Utilisation de closure pour capturer 'i'
            btn.bind("click", lambda e, idx=i: switch_tab(idx))

        container <= tablist
        container <= panels_container
        
        return container

    # ==========================================
    # 31. COMPOSANTS DE FORMULAIRE (TEXTAREA)
    # ==========================================

    @staticmethod
    def Textarea(label, value="", placeholder="", rows=4, variant="simple", actions=None, on_change=None, extra_class=""):
        """
        Zone de texte multiligne.
        Gère les styles : Base, Actions Inside, Actions Outside.
        
        Args:
            label: Texte du label.
            value: Contenu initial.
            rows: Hauteur en lignes.
            variant: "simple" (standard), "inside" (boutons dedans), "outside" (boutons dessous).
            actions: Liste de boutons [{'text': 'Save', 'onclick': cb, 'variant': 'primary'}].
            on_change: Callback sur changement de texte.
        """
        t = UI.THEME
        
        container = html.DIV(Class=f"{extra_class}")
        
        # ID unique pour lier label
        txt_id = f"txt-{int(window.Math.random()*10000)}"
        
        # Le Label
        lbl = html.LABEL(For=txt_id, Class="block")
        if label:
            lbl <= html.SPAN(label, Class=f"text-sm font-medium {t['text_main']}")
            
        # Styles de base du Textarea
        # resize-none pour éviter de casser le layout (comme dans l'exemple HyperUI)
        base_cls = f"w-full resize-none sm:text-sm {t['text_main']} {t['input_bg']} placeholder-gray-400 focus:outline-none"
        
        # Création de l'élément Textarea
        textarea = html.TEXTAREA(
            value, 
            Id=txt_id, 
            rows=rows, 
            placeholder=placeholder
        )
        if on_change: textarea.bind("input", on_change)

        # --- Helper pour la barre d'actions ---
        def make_actions_bar(btn_list, layout_cls):
            bar = html.DIV(Class=f"flex items-center gap-2 {layout_cls}")
            for act in btn_list:
                is_primary = act.get("variant") == "primary"
                
                # Styles spécifiques aux boutons de textarea (souvent plus petits/discrets)
                if is_primary:
                    btn_style = f"rounded bg-{t['accent']}-600 px-3 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-{t['accent']}-700"
                else:
                    btn_style = f"rounded border border-transparent px-3 py-1.5 text-sm font-medium {t['text_muted']} hover:{t['text_main']} hover:{t['hover']}"
                
                btn = html.BUTTON(act["text"], type="button", Class=f"{btn_style} transition-colors")
                if act.get("onclick"):
                    btn.bind("click", act["onclick"])
                bar <= btn
            return bar

        # --- Assemblage selon Variant ---
        
        if variant == "inside":
            # Wrapper avec bordure qui contient le textarea ET les boutons
            wrapper = html.DIV(
                Class=f"relative mt-0.5 overflow-hidden rounded border {t['border']} shadow-sm focus-within:ring-1 focus-within:ring-{t['accent']}-600"
            )
            
            # Textarea sans bordure (border-none) car c'est le wrapper qui l'a
            textarea.class_name = f"{base_cls} border-none focus:ring-0"
            wrapper <= textarea
            
            # Barre d'actions (padding interne, aligné à droite)
            if actions:
                # Ajout d'une ligne de séparation subtile ou juste padding
                wrapper <= make_actions_bar(actions, "justify-end p-2 bg-gray-50 dark:bg-gray-800/50")
                
            lbl <= wrapper
            container <= lbl
            
        else: # simple ou outside
            # Textarea avec sa propre bordure
            textarea.class_name = f"{base_cls} mt-0.5 rounded border {t['border']} shadow-sm focus:border-{t['accent']}-500 focus:ring-1 focus:ring-{t['accent']}-500"
            lbl <= textarea
            container <= lbl
            
            # Barre d'actions à l'extérieur (mt-2)
            if variant == "outside" and actions:
                container <= make_actions_bar(actions, "mt-2 justify-end")

        return container

    # ==========================================
    # 32. COMPOSANTS DE DONNÉES (TIMELINE)
    # ==========================================

    @staticmethod
    def Timeline(events, variant="vertical", extra_class=""):
        """
        Chronologie d'événements.
        
        Args:
            events: Liste de dicts [{'date': '12/02/2025', 'title': 'Kickoff', 'desc': 'Lorem...'}]
            variant: "vertical" (gauche), "vertical-middle" (alterné), "horizontal" (ligne).
        """
        t = UI.THEME
        
        container = html.OL(Class=f"relative {extra_class}")
        
        # --- Configuration de la ligne de fond (Before pseudo-element replacement) ---
        # En Brython/HTML pur, pas de pseudo-elements faciles dynamiques.
        # On utilise une DIV absolue pour la ligne.
        
        if variant == "horizontal":
            container.classList.add("flex", "gap-8")
            line = html.DIV(Class="absolute top-1.5 left-0 w-full h-0.5 rounded-full bg-gray-200 dark:bg-gray-700")
        elif variant == "vertical-middle":
            container.classList.add("space-y-8")
            line = html.DIV(Class="absolute top-0 left-1/2 h-full w-0.5 -translate-x-1/2 rounded-full bg-gray-200 dark:bg-gray-700")
        else: # vertical standard
            container.classList.add("space-y-8")
            line = html.DIV(Class="absolute top-0 left-1.5 h-full w-0.5 rounded-full bg-gray-200 dark:bg-gray-700")
            
        container <= line
        
        for i, ev in enumerate(events):
            title = ev.get("title", "")
            date = ev.get("date", "")
            desc = ev.get("desc", "")
            
            # Point (Rond coloré)
            dot = html.SPAN(Class=f"size-3 shrink-0 rounded-full bg-{t['accent']}-600")
            
            # Contenu Texte
            content_div = html.DIV(Class="-mt-2" if "vertical" in variant else "mt-4")
            content_div <= html.TIME(date, Class=f"text-xs font-medium {t['text_muted']}")
            content_div <= html.H3(title, Class=f"text-lg font-bold {t['text_main']}")
            if desc:
                content_div <= html.P(desc, Class=f"mt-0.5 text-sm {t['text_muted']}")
            
            # Assemblage selon Variant
            if variant == "vertical-middle":
                # Layout Grille 2 colonnes pour alternance
                # odd:-me-3 even:-ms-3 pour coller à la ligne centrale
                li = html.LI(Class="relative grid grid-cols-2 gap-8 items-center") # Ajustement gap
                
                # Côté Gauche ou Droite selon pair/impair
                is_even = (i % 2 == 1)
                
                # Wrapper interne pour flex direction
                wrapper_cls = "relative flex items-start gap-4"
                if not is_even: # Impair (Gauche) -> Texte à droite, Dot à droite (flex-row-reverse text-right)
                    wrapper_cls += " flex-row-reverse text-right pr-4" # pr-4 pour écarter de la ligne
                    # Le div vide est à droite
                    wrapper_div = html.DIV(Class=wrapper_cls)
                    wrapper_div <= dot
                    wrapper_div <= content_div
                    li <= wrapper_div
                    li <= html.DIV() # Espace vide à droite
                else: # Pair (Droite) -> Texte à gauche (standard), Dot à gauche
                    wrapper_cls += " pl-4"
                    # Le div vide est à gauche
                    li <= html.DIV()
                    wrapper_div = html.DIV(Class=wrapper_cls)
                    wrapper_div <= dot
                    wrapper_div <= content_div
                    li <= wrapper_div
                    
                container <= li
                
            elif variant == "horizontal":
                li = html.LI(Class="relative") # -mt-1.5 géré par flex align ?
                # Pour aligner le point sur la ligne (top-1.5 = 6px, size-3 = 12px -> centre)
                # On met le dot en absolu ou on ajuste les marges
                # Dans l'exemple HyperUI : relative -mt-1.5 sur le LI
                
                # Ajustement simple : Dot block
                dot.classList.add("block")
                li <= dot
                li <= content_div
                container <= li
                
            else: # Vertical Standard
                li = html.LI(Class="relative flex items-start gap-4")
                li <= dot
                li <= content_div
                container <= li
                
        return container

    # ==========================================
    # 33. COMPOSANTS DE FEEDBACK (TOASTS)
    # ==========================================

    @staticmethod
    def Toast(title, message, variant="info", style="standard", action=None, duration=5000, extra_class=""):
        """
        Notification Toast temporaire.
        
        Args:
            title: Titre (ex: "Success").
            message: Texte descriptif.
            variant: "success", "error", "warning", "info".
            style: "standard" (fond coloré léger) ou "standout" (bordure gauche).
            action: Dict {'text': 'Undo', 'onclick': cb} (optionnel).
            duration: Temps en ms avant disparition (0 pour infini).
        """
        # Configuration des couleurs et icônes
        config = {
            "success": {
                "color": "green",
                "icon": "M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            },
            "error": {
                "color": "red",
                "icon": "M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
            },
            "warning": {
                "color": "amber",
                "icon": "M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z"
            },
            "info": {
                "color": "blue",
                "icon": "m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"
            }
        }
        
        cfg = config.get(variant, config["info"])
        c = cfg["color"]
        
        # --- Conteneur Toast ---
        # Position fixed en bas à droite (standard pour les notifications)
        # animate-in slide-in-from-right pour l'effet d'entrée
        base_cls = (
            f"fixed bottom-4 right-4 z-[60] w-full max-w-sm overflow-hidden "
            f"animate-in slide-in-from-right fade-in duration-300 shadow-lg {extra_class}"
        )
        
        # Styles spécifiques
        if style == "standout":
            # Bordure gauche épaisse
            colors = f"bg-{c}-50 border-s-4 border-{c}-700 p-4 dark:bg-{c}-900 dark:border-{c}-600"
            container = html.DIV(role="alert", Class=f"{base_cls} {colors}")
            
            # Layout Flex simple
            flex = html.DIV(Class=f"flex items-center gap-2 text-{c}-700 dark:text-{c}-200")
            flex <= UI.Icon(cfg["icon"], size=24) # size-6
            flex <= html.STRONG(title, Class=f"block font-medium text-{c}-800 dark:text-{c}-100")
            container <= flex
            
            container <= html.P(message, Class=f"mt-1 text-sm text-{c}-700 dark:text-{c}-200")
            
        else: # Standard / With Action
            # Fond coloré léger et bordure fine
            colors = f"bg-{c}-50 border border-{c}-500 rounded-md p-4 dark:bg-{c}-800 dark:border-{c}-400"
            container = html.DIV(role="alert", Class=f"{base_cls} {colors}")
            
            wrapper = html.DIV(Class="flex items-start gap-4")
            
            # Icône
            wrapper <= UI.Icon(cfg["icon"], size=24, extra_class=f"-mt-0.5 text-{c}-700 dark:text-{c}-200")
            
            # Contenu
            content_div = html.DIV(Class="flex-1")
            content_div <= html.STRONG(title, Class=f"block font-medium text-{c}-800 dark:text-{c}-100")
            content_div <= html.P(message, Class=f"mt-0.5 text-sm text-{c}-700 dark:text-{c}-200")
            
            # Bouton d'Action (Optionnel)
            if action:
                btn = html.BUTTON(
                    action["text"], 
                    type="button",
                    Class=f"mt-2 inline-block rounded-sm bg-{c}-600 px-4 py-2 text-sm font-medium text-white hover:bg-transparent hover:text-{c}-600 border border-{c}-600 transition-colors"
                )
                
                def _on_action(ev):
                    if action.get("onclick"): action["onclick"](ev)
                    container.remove() # Fermer après action
                    
                btn.bind("click", _on_action)
                content_div <= btn
                
            wrapper <= content_div
            container <= wrapper

        # --- Gestionnaires ---
        
        # Ajout au DOM
        document.body <= container
        
        # Auto-remove
        if duration > 0:
            def _remove():
                # Animation de sortie (optionnel, nécessite gestion CSS plus complexe pour fade-out)
                # Ici on retire brutalement pour simplifier Brython
                if container.parent: container.remove()
            window.setTimeout(_remove, duration)
            
        # Click to dismiss (manuel)
        container.bind("click", lambda e: container.remove())
        
        return container

    # ==========================================
    # 34. COMPOSANTS DE FORMULAIRE (TOGGLE)
    # ==========================================

    @staticmethod
    def Toggle(label, value=False, variant="base", on_change=None, extra_class=""):
        """
        Interrupteur On/Off (Switch).
        
        Args:
            label: Texte affiché à côté.
            value: État initial (True/False).
            variant: "base" (Simple), "icon" (Avec X/Check), "material" (Fine barre), "apple" (iOS style).
            on_change: Callback (nouvelle valeur booléenne).
        """
        t = UI.THEME
        
        # Wrapper pour aligner le Toggle et le Label texte
        container = html.DIV(Class=f"flex items-center gap-3 {extra_class}")
        
        # ID unique
        tog_id = f"tog-{int(window.Math.random()*10000)}"
        
        # --- 1. Configuration des Styles selon Variant ---
        
        # Style du conteneur (Track)
        # has-checked:... permet de changer la couleur du fond quand l'input caché est checked
        base_track = f"relative block transition-colors [-webkit-tap-highlight-color:transparent] cursor-pointer"
        
        if variant == "material":
            # Barre fine
            track_cls = f"{base_track} h-4 w-10 rounded-full bg-gray-300 dark:bg-gray-600"
            # Le material ne change pas la couleur du track, mais du thumb (souvent). 
            # Simplification: on change le track comme les autres pour l'état actif.
            track_active = f"has-checked:bg-{t['accent']}-600/50" # Couleur plus claire pour la barre
        elif variant == "apple":
            track_cls = f"{base_track} h-8 w-14 rounded-full bg-gray-300 dark:bg-gray-600"
            track_active = f"has-checked:bg-{t['accent']}-600"
        else: # base / icon
            track_cls = f"{base_track} h-8 w-14 rounded-full bg-gray-300 dark:bg-gray-600"
            track_active = f"has-checked:bg-{t['accent']}-600"
            
        label_el = html.LABEL(For=tog_id, Class=f"{track_cls} {track_active}")
        
        # --- 2. Input Caché ---
        inp = html.INPUT(type="checkbox", Id=tog_id, Class="peer sr-only")
        if value: inp.checked = True
        
        if on_change:
            inp.bind("change", lambda e: on_change(e.target.checked))
            
        label_el <= inp
        
        # --- 3. Le "Thumb" (Rond qui bouge) ---
        
        if variant == "material":
            # Material Thumb : Plus gros que la barre, centré verticalement
            thumb_cls = (
                f"absolute top-1/2 -left-1 -translate-y-1/2 size-6 rounded-full shadow-md transition-all duration-200 "
                f"bg-white dark:bg-gray-200 border border-gray-200 "
                f"peer-checked:translate-x-full peer-checked:border-{t['accent']}-600 peer-checked:bg-{t['accent']}-600"
            )
            thumb = html.SPAN(Class=thumb_cls)
            
        elif variant == "apple":
            # Apple Thumb : Animation de largeur
            thumb_cls = (
                f"absolute inset-y-0 start-0 m-1 size-6 rounded-full bg-white shadow-sm transition-all "
                f"peer-checked:start-8" 
                # Note: L'effet de morphing exact d'Apple (w-2 -> w-6) est complexe en pure utility classes sans CSS custom
                # On reste sur un slide propre.
            )
            thumb = html.SPAN(Class=thumb_cls)
            
        elif variant == "icon":
            # Thumb avec Icônes
            thumb_cls = (
                f"absolute inset-y-0 start-0 m-1 size-6 rounded-full bg-white dark:bg-gray-900 shadow-sm transition-all "
                f"peer-checked:start-6 flex items-center justify-center text-gray-400 peer-checked:text-{t['accent']}-600"
            )
            thumb = html.SPAN(Class=thumb_cls)
            
            # Icone X (visible quand unchecked)
            # peer-checked sur l'input rend cet élément hidden
            icon_x = UI.Icon("M6 18L18 6M6 6l12 12", size=14)
            icon_x.classList.add("block", "peer-checked:hidden") # Hack: on ne peut pas utiliser peer ici car on est DANS le peer-checked
            # Correction: Le CSS Tailwind "peer-checked:*:first:hidden" fonctionne si appliqué au parent.
            # En Brython, on va utiliser une logique simple de classes CSS standard conditionnelles au parent input ? 
            # Non, le plus simple est de mettre 2 icones et d'utiliser des classes utilitaires directes.
            
            # Astuce pour les icônes inside :
            # On utilise le CSS du parent Thumb pour cacher/montrer les enfants
            # Mais "peer" ne marche que pour les frères suivants.
            # Ici Thumb est frère de Input. Donc dans Thumb, on ne peut pas savoir l'état de Input facilement sans 'has-checked' du parent ou 'peer-checked' appliqué au Thumb.
            
            # Approche HyperUI : 
            # Le thumb a : "peer-checked:*:first:hidden *:last:hidden peer-checked:*:last:block"
            
            # SVG Croix (First)
            svg_x = html.SVG(xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke_width="2", stroke="currentColor", Class="size-4 block")
            svg_x <= html.PATH(stroke_linecap="round", stroke_linejoin="round", d="M6 18L18 6M6 6l12 12")
            
            # SVG Check (Last)
            svg_c = html.SVG(xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke_width="2", stroke="currentColor", Class="size-4 hidden")
            svg_c <= html.PATH(stroke_linecap="round", stroke_linejoin="round", d="m4.5 12.75 6 6 9-13.5")
            
            # On ajoute des classes au Thumb pour gérer l'affichage des enfants
            # [&>svg:first-child]:block peer-checked:[&>svg:first-child]:hidden
            # [&>svg:last-child]:hidden peer-checked:[&>svg:last-child]:block
            thumb.classList.add("[&>svg:first-child]:block", "peer-checked:[&>svg:first-child]:hidden")
            thumb.classList.add("[&>svg:last-child]:hidden", "peer-checked:[&>svg:last-child]:block")
            
            thumb <= svg_x
            thumb <= svg_c
            
        else: # base
            thumb_cls = (
                f"absolute inset-y-0 start-0 m-1 size-6 rounded-full bg-white dark:bg-gray-900 shadow-sm transition-all "
                f"peer-checked:start-6"
            )
            thumb = html.SPAN(Class=thumb_cls)
            
        label_el <= thumb
        
        container <= label_el
        
        # Label Texte
        if label:
            # Click sur le texte toggle aussi l'input grâce à l'ID ? Non, il faut un label for.
            # On crée un 2ème label pointant vers le même ID pour le texte
            text_lbl = html.LABEL(label, For=tog_id, Class=f"text-sm font-medium {t['text_main']} cursor-pointer select-none")
            container <= text_lbl
            
        return container
    
    # ==========================================
    # 35. COMPOSANTS DE NAVIGATION (VERTICAL MENU)
    # ==========================================

    @staticmethod
    def VerticalMenu(data, extra_class=""):
        """
        Menu vertical (Sidebar).
        Gère les icônes, badges, accordéons et sections divisées.
        
        Args:
            data: 
                - Liste d'items: [{'label': 'Home', 'icon': 'home'}, ...]
                - Liste de listes (Sections): [[item1, item2], [item3, item4]]
            
            Structure d'un item (dict):
                - label: Texte.
                - icon: Nom de l'icône (opt).
                - badge: Texte/Nombre à droite (opt).
                - active: Booléen (style sélectionné).
                - onclick: Callback.
                - subitems: Liste d'items enfants (crée un accordéon).
        """
        t = UI.THEME
        
        # Détection du mode "Divided" (Liste de listes)
        is_divided = isinstance(data[0], list) if data else False
        
        # --- Helper: Rendu d'un lien ou résumé ---
        def render_link_content(item, is_summary=False):
            # Wrapper principal du contenu (Flex)
            # group pour gérer le hover du badge
            content = html.DIV(Class="flex items-center justify-between w-full")
            
            # Partie Gauche (Icon + Label)
            left = html.DIV(Class="flex items-center gap-2")
            if item.get("icon"):
                # Opacity 75 pour l'icône inactive
                icon_cls = "size-5 opacity-75"
                left <= UI.Icon(item["icon"], size=20, extra_class=icon_cls)
            left <= html.SPAN(item.get("label", ""), Class="text-sm font-medium")
            content <= left
            
            # Partie Droite (Badge ou Chevron)
            if is_summary:
                # Chevron rotatif pour l'accordéon
                chevron = UI.Icon("M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z", size=20)
                chevron.classList.add("shrink-0", "transition", "duration-300", "group-open:-rotate-180")
                content <= chevron
            elif item.get("badge"):
                # Badge
                bg_badge = "bg-gray-100 text-gray-600 group-hover:bg-gray-200 group-hover:text-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:group-hover:bg-gray-700"
                content <= html.SPAN(str(item["badge"]), Class=f"shrink-0 rounded-full px-3 py-0.5 text-xs {bg_badge}")
                
            return content

        # --- Helper: Rendu d'un Item (<li>) ---
        def render_item(item):
            li = html.LI()
            
            # Styles communs
            base_cls = "group flex items-center justify-between rounded-lg px-4 py-2 text-sm font-medium transition-colors w-full text-left"
            
            # État Actif / Inactif
            if item.get("active"):
                state_cls = f"bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-200"
            else:
                state_cls = f"text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-200"
            
            # CAS 1: Accordéon (Sous-menus)
            if item.get("subitems"):
                details = html.DETAILS(Class="group [&_summary::-webkit-details-marker]:hidden")
                summary = html.SUMMARY(Class=f"{base_cls} {state_cls} cursor-pointer")
                summary <= render_link_content(item, is_summary=True)
                
                # Liste des enfants
                ul_sub = html.UL(Class="mt-2 space-y-1 px-4")
                for sub in item["subitems"]:
                    ul_sub <= render_item(sub)
                    
                details <= summary
                details <= ul_sub
                li <= details
                
            # CAS 2: Lien Standard
            else:
                a = html.A(href="#", Class=f"{base_cls} {state_cls}")
                if item.get("onclick"):
                    a.bind("click", item["onclick"])
                    
                a <= render_link_content(item)
                li <= a
                
            return li

        # --- Construction du Conteneur ---
        
        if is_divided:
            # Mode "Divided Sections"
            # Un root UL qui contient des LI (sections) séparés par des lignes
            container = html.DIV(Class=f"flow-root {extra_class}")
            root_ul = html.UL(Class="-my-2 divide-y divide-gray-100 dark:divide-gray-800")
            
            for section_items in data:
                section_li = html.LI(Class="py-2")
                sub_ul = html.UL(Class="space-y-1")
                for item in section_items:
                    sub_ul <= render_item(item)
                section_li <= sub_ul
                root_ul <= section_li
                
            container <= root_ul
            return container
            
        else:
            # Mode Standard (Liste simple)
            ul = html.UL(Class=f"space-y-1 {extra_class}")
            for item in data:
                ul <= render_item(item)
            return ul
        
        # ==========================================
    # 36. COMPOSANTS DE MARKETING (ANNOUNCEMENTS)
    # ==========================================

    @staticmethod
    def Announcement(text, link_text=None, link_url="#", variant="base", dismissible=False, extra_class=""):
        """
        Bannière d'annonce (Top/Bottom bar).
        
        Args:
            text: Message principal.
            link_text: Texte du lien (optionnel).
            link_url: URL du lien.
            variant: "base" (statique), "fixed" (bas écran), "floating" (flottant bas).
            dismissible: Affiche une croix pour fermer.
        """
        t = UI.THEME
        
        # Styles de base (Fond gris léger pour se distinguer du header blanc)
        bg_cls = "bg-gray-100 dark:bg-gray-800 border-gray-200 dark:border-gray-700"
        
        # Contenu Texte
        content_p = html.P(Class=f"text-center font-medium {t['text_main']}")
        content_p <= html.SPAN(text + " ")
        if link_text:
            content_p <= html.A(link_text, href=link_url, Class=f"inline-block underline hover:{t['accent_text']}")

        # Bouton Fermer (si dismissible)
        btn_dismiss = None
        if dismissible:
            btn_dismiss = html.BUTTON(
                type="button", 
                aria_label="Dismiss", 
                Class=f"rounded border {t['border']} {t['panel_bg']} p-1.5 shadow-sm transition-colors hover:{t['hover']}"
            )
            btn_dismiss <= UI.Icon("M6 18L18 6M6 6l12 12", size=20) # size-5

        # --- Construction selon Variant ---
        
        if variant == "floating":
            # Wrapper invisible pour le positionnement fixed
            container = html.DIV(Class=f"fixed inset-x-0 bottom-0 z-50 p-4 {extra_class}")
            
            # La boîte visible
            box = html.DIV(Class=f"rounded border shadow-lg {bg_cls} px-4 py-3")
            
            if dismissible:
                box.classList.add("flex", "items-center", "justify-between", "gap-4")
                box <= html.SPAN() # Spacer gauche pour équilibrer
                box <= content_p
                box <= btn_dismiss
                # Action
                btn_dismiss.bind("click", lambda e: container.remove())
            else:
                box <= content_p
                
            container <= box
            
        elif variant == "fixed":
            # Barre fixée en bas (border-t)
            container = html.DIV(Class=f"fixed inset-x-0 bottom-0 z-50 border-t {bg_cls} px-4 py-3 {extra_class}")
            
            if dismissible:
                container.classList.add("flex", "items-center", "justify-between", "gap-4")
                container <= html.SPAN()
                container <= content_p
                container <= btn_dismiss
                btn_dismiss.bind("click", lambda e: container.remove())
            else:
                container <= content_p
                
        else: # Base (Static)
            # Barre statique (border-b souvent utilisée en haut de page)
            container = html.DIV(Class=f"border-b {bg_cls} px-4 py-3 {extra_class}")
            
            if dismissible:
                container.classList.add("flex", "items-center", "justify-between", "gap-4")
                container <= html.SPAN()
                container <= content_p
                container <= btn_dismiss
                btn_dismiss.bind("click", lambda e: container.remove())
            else:
                container <= content_p

        return container

    # ==========================================
    # 37. COMPOSANTS MARKETING (HERO/BANNER)
    # ==========================================

    @staticmethod
    def Hero(title, subtitle, buttons=None, image=None, highlight_text=None, align="center", full_height=False, extra_class=""):
        """
        Section Hero / Bannière principale.
        
        Args:
            title: Titre principal (H1).
            subtitle: Texte descriptif.
            buttons: Liste de dicts [{'text': 'Start', 'variant': 'primary', 'onclick': cb}].
            image: URL d'image (str) ou Élément HTML/SVG. Si présent, active le layout Split.
            highlight_text: Partie du titre à mettre en couleur d'accent.
            align: "center" ou "left" (ignoré si image présente -> split layout).
            full_height: Si True, prend toute la hauteur de l'écran (h-screen).
        """
        t = UI.THEME
        
        # Section Container
        # lg:h-screen si demandé
        h_cls = "lg:grid lg:h-screen lg:place-content-center" if full_height else ""
        section = html.SECTION(Class=f"{t['panel_bg']} {h_cls} {extra_class}")
        
        # Wrapper de contenu (Max width)
        container_cls = "mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8 lg:py-32"
        if image:
            container_cls += " md:grid md:grid-cols-2 md:items-center md:gap-8"
            
        content_wrapper = html.DIV(Class=container_cls)
        
        # --- Bloc Texte ---
        text_align = "text-center" if align == "center" and not image else "text-left"
        text_div = html.DIV(Class=f"max-w-prose {text_align} mx-auto" if align=="center" and not image else "")
        
        # 1. Titre H1 avec Highlight
        h1 = html.H1(Class=f"text-4xl font-bold {t['text_main']} sm:text-5xl")
        
        if highlight_text and highlight_text in title:
            # On découpe le titre pour insérer le span coloré
            parts = title.split(highlight_text)
            h1 <= html.SPAN(parts[0])
            h1 <= html.STRONG(f" {highlight_text} ", Class=f"text-{t['accent']}-600")
            if len(parts) > 1: h1 <= html.SPAN(parts[1])
        else:
            h1.text = title
            
        text_div <= h1
        
        # 2. Sous-titre
        if subtitle:
            text_div <= html.P(subtitle, Class=f"mt-4 text-base text-pretty {t['text_muted']} sm:text-lg/relaxed")
            
        # 3. Boutons
        if buttons:
            # Alignement des boutons
            btn_align = "justify-center" if align == "center" and not image else "justify-start"
            btn_wrapper = html.DIV(Class=f"mt-8 flex flex-wrap gap-4 {btn_align}")
            
            for btn_data in buttons:
                is_primary = btn_data.get("variant") == "primary"
                
                if is_primary:
                    b_cls = f"rounded border border-{t['accent']}-600 bg-{t['accent']}-600 px-12 py-3 text-sm font-medium text-white hover:bg-transparent hover:text-{t['accent']}-600 focus:ring-3 focus:outline-hidden sm:w-auto active:text-opacity-75 transition-colors"
                else:
                    b_cls = f"rounded border {t['border']} px-12 py-3 text-sm font-medium {t['text_main']} hover:{t['accent_text']} hover:{t['panel_bg']} focus:ring-3 focus:outline-hidden sm:w-auto transition-colors"
                
                # On utilise A si href, sinon BUTTON
                tag = html.A if btn_data.get("href") else html.BUTTON
                kwargs = {"href": btn_data.get("href", "#")} if tag == html.A else {"type": "button"}
                
                btn_el = tag(btn_data["text"], Class=b_cls, **kwargs)
                if btn_data.get("onclick"):
                    btn_el.bind("click", btn_data["onclick"])
                    
                btn_wrapper <= btn_el
                
            text_div <= btn_wrapper
            
        content_wrapper <= text_div
        
        # --- Bloc Image (Optionnel) ---
        if image:
            img_div = html.DIV(Class="mt-8 md:mt-0")
            if isinstance(image, str):
                # URL image
                img_el = html.IMG(src=image, alt=title, Class="w-full rounded-lg shadow-xl")
                img_div <= img_el
            else:
                # Élément HTML/SVG direct
                img_div <= image
            content_wrapper <= img_div
            
        section <= content_wrapper
        return section


    # ==========================================
    # 38. COMPOSANTS DE CONTENU (BLOG)
    # ==========================================

    @staticmethod
    def BlogCard(title, excerpt, date, image=None, link="#", tags=None, variant="bordered", extra_class=""):
        """
        Carte d'article de blog / actualité.
        
        Args:
            title: Titre de l'article.
            excerpt: Résumé (coupé à 3 lignes).
            date: Date (str).
            image: URL de l'image.
            link: Lien au clic.
            tags: Liste de strings (ex: ['Tech', 'Python']).
            variant: "bordered" (Classique), "overlay" (Texte sur image), "plain" (Sans bordure).
        """
        t = UI.THEME
        
        # --- CAS 1: OVERLAY (Image de fond + Texte par dessus) ---
        if variant == "overlay" and image:
            container = html.ARTICLE(
                Class=f"relative overflow-hidden rounded-lg shadow-sm transition hover:shadow-lg {extra_class}"
            )
            
            # Image Absolute
            img_el = html.IMG(
                src=image, 
                alt=title, 
                Class="absolute inset-0 h-full w-full object-cover"
            )
            container <= img_el
            
            # Gradient Overlay + Contenu
            content_div = html.DIV(
                Class="relative bg-gradient-to-t from-gray-900/90 to-gray-900/25 pt-32 sm:pt-48 lg:pt-64"
            )
            
            inner = html.DIV(Class="p-4 sm:p-6")
            inner <= html.TIME(date, Class="block text-xs text-white/90")
            
            link_el = html.A(href=link)
            link_el <= html.H3(title, Class="mt-0.5 text-lg font-medium text-white")
            inner <= link_el
            
            inner <= html.P(excerpt, Class="mt-2 line-clamp-3 text-sm/relaxed text-white/95")
            
            content_div <= inner
            container <= content_div
            return container

        # --- CAS 2: STANDARD (Bordered / Plain) ---
        
        # Base classes
        base_cls = "overflow-hidden rounded-lg transition hover:shadow-lg"
        if variant == "bordered":
            base_cls += f" border {t['border']} shadow-sm {t['panel_bg']}"
        elif variant == "plain":
            base_cls += " group" # Pour effets hover éventuels
            
        container = html.ARTICLE(Class=f"{base_cls} {extra_class}")
        
        # Image (Top)
        if image:
            img_cls = "h-56 w-full object-cover"
            if variant == "plain": img_cls += " rounded-xl shadow-md transition group-hover:grayscale-[50%]" # Style 'Floating'
            
            img_el = html.IMG(src=image, alt=title, Class=img_cls)
            container <= img_el
            
        # Contenu (Bottom)
        # Padding diffère selon le style
        p_cls = "p-4 sm:p-6" if variant == "bordered" else "pt-4"
        
        content_div = html.DIV(Class=f"{p_cls} {t['panel_bg'] if variant=='bordered' else ''}")
        
        content_div <= html.TIME(date, Class=f"block text-xs {t['text_muted']}")
        
        link_el = html.A(href=link)
        link_el <= html.H3(title, Class=f"mt-0.5 text-lg font-medium {t['text_main']}")
        content_div <= link_el
        
        content_div <= html.P(excerpt, Class=f"mt-2 line-clamp-3 text-sm/relaxed {t['text_muted']}")
        
        # Tags (Optionnel)
        if tags:
            tags_div = html.DIV(Class="mt-4 flex flex-wrap gap-2")
            for tag in tags:
                # Badge simple coloré
                span = html.SPAN(
                    tag, 
                    Class=f"rounded-full bg-{t['accent']}-100 px-2.5 py-0.5 text-xs text-{t['accent']}-600 dark:bg-{t['accent']}-900/30 dark:text-{t['accent']}-300"
                )
                tags_div <= span
            content_div <= tags_div
            
        container <= content_div
        
        return container

    # ==========================================
    # 39. COMPOSANTS DE CONTENU (CARDS)
    # ==========================================

    @staticmethod
    def Card(title=None, content=None, image=None, footer=None, variant="vertical", url=None, tags=None, extra_class=""):
        """
        Composant Carte polyvalent.
        
        Args:
            title: Titre principal (str).
            content: Texte (str) ou Élément HTML.
            image: URL de l'image (str) ou Élément IMG/SVG.
            footer: Élément de pied de page (auteur, date, prix...).
            variant: "vertical" (Standard), "horizontal" (Row), "overlay" (Image background).
            url: Si défini, rend la carte cliquable (<a>).
            tags: Liste de badges à afficher.
        """
        t = UI.THEME
        
        # 1. Choix du Tag Racine (Article ou A)
        tag = html.A if url else html.ARTICLE
        attrs = {"href": url} if url else {}
        
        # Classes de base (Bordure, Ombre, Fond)
        base_cls = f"group relative block overflow-hidden rounded-lg border {t['border']} {t['panel_bg']} shadow-sm transition hover:shadow-lg"
        
        # --- CAS 1: OVERLAY (Image fond + Texte dessus) ---
        if variant == "overlay":
            container = tag(Class=f"{base_cls} h-64 sm:h-80 lg:h-96 {extra_class}", **attrs)
            
            # Image Absolute
            if image:
                src = image if isinstance(image, str) else image.src
                img_el = html.IMG(
                    src=src, 
                    alt=title, 
                    Class="absolute inset-0 h-full w-full object-cover transition-opacity group-hover:opacity-90"
                )
                container <= img_el
                
            # Contenu Overlay (Gradient pour lisibilité)
            overlay_content = html.DIV(Class="relative h-full flex flex-col justify-end bg-gradient-to-t from-gray-900/90 to-transparent p-4 sm:p-6")
            
            if tags:
                tag_span = html.P(tags[0], Class=f"text-sm font-medium uppercase tracking-widest text-{t['accent']}-400")
                overlay_content <= tag_span
                
            if title:
                overlay_content <= html.H3(title, Class="mt-2 text-xl font-bold text-white")
                
            if content:
                overlay_content <= html.DIV(content, Class="mt-2 text-white/90 line-clamp-3")
                
            container <= overlay_content
            return container

        # --- CAS 2: HORIZONTAL (Podcast / Forum Style) ---
        elif variant == "horizontal":
            container = tag(Class=f"{base_cls} flex flex-row {extra_class}", **attrs)
            
            # Image à gauche
            if image:
                img_div = html.DIV(Class="w-32 sm:w-48 shrink-0")
                if isinstance(image, str):
                    img_div <= html.IMG(src=image, alt=title, Class="h-full w-full object-cover")
                else:
                    image.classList.add("h-full", "w-full", "object-cover")
                    img_div <= image
                container <= img_div
                
            # Corps à droite
            body = html.DIV(Class="flex flex-1 flex-col justify-between p-4 sm:p-6")
            
            # Titre + Contenu
            top_block = html.DIV()
            if title: top_block <= html.H3(title, Class=f"font-bold uppercase {t['text_main']}")
            if content: 
                desc = html.P(content, Class=f"mt-2 line-clamp-3 text-sm/relaxed {t['text_muted']}") if isinstance(content, str) else content
                top_block <= desc
            body <= top_block
            
            # Footer / Tags
            if footer or tags:
                foot_div = html.DIV(Class="mt-4 flex items-end justify-between")
                if tags:
                    tags_div = html.DIV(Class="flex gap-2")
                    for tag_txt in tags: tags_div <= UI.Badge(tag_txt, "gray")
                    foot_div <= tags_div
                if footer: foot_div <= footer
                body <= foot_div
                
            container <= body
            return container

        # --- CAS 3: VERTICAL (Standard Blog/Product) ---
        else:
            container = tag(Class=f"{base_cls} {extra_class}", **attrs)
            
            # Image Top
            if image:
                img_cls = "h-56 w-full object-cover"
                if isinstance(image, str):
                    container <= html.IMG(src=image, alt=title, Class=img_cls)
                else:
                    image.classList.add("h-56", "w-full", "object-cover")
                    container <= image
            
            # Body
            body = html.DIV(Class="p-4 sm:p-6")
            
            if title: 
                body <= html.H3(title, Class=f"text-lg font-medium {t['text_main']}")
                
            if content:
                desc = html.P(content, Class=f"mt-2 line-clamp-3 text-sm/relaxed {t['text_muted']}") if isinstance(content, str) else content
                body <= desc
                
            # Footer (Date, Auteur, Prix...)
            if footer:
                # Ligne de séparation ou margin
                foot_wrap = html.DIV(Class="mt-4 flex items-center gap-4")
                if isinstance(footer, list):
                    for item in footer: foot_wrap <= item
                else:
                    foot_wrap <= footer
                body <= foot_wrap
                
            container <= body
            return container
        
    # ==========================================
    # 40. COMPOSANTS E-COMMERCE (CART)
    # ==========================================

    @staticmethod
    def Cart(items, variant="popup", summary=None, on_checkout=None, on_close=None, on_remove=None, extra_class=""):
        """
        Panier d'achat (Popup ou Page complète).
        
        Args:
            items: Liste de dicts [{'title': 'T-Shirt', 'image': 'url', 'meta': {'Size': 'M'}, 'qty': 1, 'price': '$20'}].
            variant: "popup" (latéral/modal) ou "page" (pleine largeur avec résumé détaillé).
            summary: Dict pour le pied de page (ex: {'Subtotal': '$50', 'Total': '$60'}).
            on_checkout: Callback bouton Checkout.
            on_close: Callback bouton fermeture (popup).
            on_remove: Callback suppression item (reçoit l'index).
        """
        t = UI.THEME
        
        # --- Helper: Rendu d'un item ---
        def render_item(idx, item):
            li = html.LI(Class="flex items-center gap-4")
            
            # Image
            if item.get("image"):
                li <= html.IMG(
                    src=item["image"], 
                    alt=item.get("title", ""), 
                    Class="size-16 rounded object-cover"
                )
                
            # Infos
            info = html.DIV()
            info <= html.H3(item.get("title", "Product"), Class=f"text-sm {t['text_main']}")
            
            # Métadonnées (Taille, Couleur...)
            if item.get("meta"):
                dl = html.DL(Class=f"mt-0.5 space-y-px text-[10px] {t['text_muted']}")
                for k, v in item["meta"].items():
                    div = html.DIV()
                    div <= html.DT(f"{k}: ", Class="inline")
                    div <= html.DD(v, Class="inline")
                    dl <= div
                info <= dl
            li <= info
            
            # Actions (Quantité / Delete)
            actions = html.DIV(Class="flex flex-1 items-center justify-end gap-2")
            
            # Input Quantité (Simplifié)
            qty = item.get("qty", 1)
            inp = html.INPUT(
                type="number", min="1", value=qty,
                Class=f"h-8 w-12 rounded border {t['border']} {t['input_bg']} {t['text_main']} p-0 text-center text-xs focus:outline-none"
            )
            actions <= inp
            
            # Bouton Supprimer
            btn_del = html.BUTTON(Class=f"{t['text_muted']} transition hover:text-red-600")
            btn_del <= html.SPAN("Remove", Class="sr-only")
            btn_del <= UI.Icon("trash", size=16)
            if on_remove:
                btn_del.bind("click", lambda e: on_remove(idx))
            actions <= btn_del
            
            li <= actions
            return li

        # --- Construction selon Variant ---
        
        if variant == "popup":
            # Style Modal / Sidebar
            container = html.DIV(
                Class=f"relative w-screen max-w-sm border {t['border']} {t['panel_bg']} px-4 py-8 sm:px-6 lg:px-8 {extra_class}",
                aria_modal="true", role="dialog"
            )
            
            # Bouton Fermer
            if on_close:
                btn_close = html.BUTTON(Class=f"absolute end-4 top-4 {t['text_muted']} transition hover:scale-110")
                btn_close <= UI.Icon("x", size=20)
                btn_close.bind("click", on_close)
                container <= btn_close
                
            # Liste
            ul = html.UL(Class="mt-4 space-y-4")
            for i, item in enumerate(items):
                ul <= render_item(i, item)
            
            wrapper = html.DIV(Class="mt-4 space-y-6")
            wrapper <= ul
            
            # Footer Simple
            footer_div = html.DIV(Class="space-y-4 text-center")
            btn_check = UI.Button("Checkout", width="full", variant="primary")
            if on_checkout: btn_check.bind("click", on_checkout)
            
            link_cont = html.A("Continue shopping", href="#", Class=f"inline-block text-sm {t['text_muted']} underline underline-offset-4 hover:{t['text_main']}")
            
            footer_div <= btn_check
            footer_div <= link_cont
            wrapper <= footer_div
            
            container <= wrapper
            return container

        else: # variant == "page"
            # Style Page Complète
            container = html.SECTION(Class=f"{extra_class}")
            max_w = html.DIV(Class="mx-auto max-w-3xl")
            
            # Header
            header = html.HEADER(Class="text-center")
            header <= html.H1("Your Cart", Class=f"text-xl font-bold {t['text_main']} sm:text-3xl")
            max_w <= header
            
            # Liste
            content_mt = html.DIV(Class="mt-8")
            ul = html.UL(Class="space-y-4")
            for i, item in enumerate(items):
                ul <= render_item(i, item)
            content_mt <= ul
            
            # Résumé Détaillé (Subtotal, VAT, Total)
            if summary:
                footer_border = html.DIV(Class=f"mt-8 flex justify-end border-t {t['border']} pt-8")
                summary_box = html.DIV(Class="w-screen max-w-lg space-y-4")
                
                dl = html.DL(Class=f"space-y-0.5 text-sm {t['text_muted']}")
                
                for label, value in summary.items():
                    # Si c'est le Total, on le met en gros
                    is_total = label.lower() == "total"
                    row_cls = "flex justify-between !text-base font-medium" if is_total else "flex justify-between"
                    val_cls = f"{t['text_main']}" if is_total else ""
                    
                    div = html.DIV(Class=row_cls)
                    div <= html.DT(label)
                    div <= html.DD(value, Class=val_cls)
                    dl <= div
                    
                summary_box <= dl
                
                # Bouton Checkout AlignRight
                btn_row = html.DIV(Class="flex justify-end")
                btn_check = UI.Button("Checkout", variant="primary")
                if on_checkout: btn_check.bind("click", on_checkout)
                btn_row <= btn_check
                
                summary_box <= btn_row
                footer_border <= summary_box
                content_mt <= footer_border
                
            max_w <= content_mt
            container <= max_w
            return container

    # ==========================================
    # 41. COMPOSANTS DE FORMULAIRE (CONTACT)
    # ==========================================

    @staticmethod
    def ContactForm(fields, on_submit=None, layout="simple", contact_details=None, extra_class=""):
        """
        Générateur de formulaire de contact.
        
        Args:
            fields: Liste de dicts définissant les champs.
                    Ex: {'id': 'name', 'label': 'Name', 'type': 'text', 'placeholder': '...'}
                    Types supportés: text, email, tel, textarea, select, checkboxes.
                    Pour grid: ajouter 'span': 2 pour prendre toute la largeur.
            on_submit: Callback (reçoit un dict des valeurs).
            layout: "simple" (stack), "grid" (2 colonnes), "split" (info à gauche).
            contact_details: Dict pour le layout 'split' {'phone': '...', 'email': '...', 'address': '...'}.
        """
        t = UI.THEME
        
        # --- Helper: Rendu d'un champ ---
        def render_field(f):
            f_type = f.get("type", "text")
            f_id = f.get("id", f"field-{int(window.Math.random()*1000)}")
            label_text = f.get("label", "")
            ph = f.get("placeholder", "")
            
            # Wrapper du champ
            # Gestion du Col Span pour le layout Grid
            span_cls = "md:col-span-2" if f.get("span") == 2 else ""
            wrapper = html.DIV(Class=span_cls)
            
            # Label
            if f_type != "checkboxes":
                wrapper <= html.LABEL(label_text, For=f_id, Class=f"block text-sm font-medium {t['text_main']}")

            # Input styles
            # Note: bg-white sur light mode pour contraste avec le fond gris du form
            base_input = (
                f"mt-1 w-full rounded-lg border {t['border']} focus:border-{t['accent']}-500 focus:ring-{t['accent']}-500 focus:outline-none "
                f"bg-white dark:bg-gray-900 {t['text_main']} sm:text-sm p-2.5"
            )

            # Rendu selon le type
            if f_type == "textarea":
                wrapper <= html.TEXTAREA(Id=f_id, rows=4, placeholder=ph, Class=f"{base_input} resize-none")
                
            elif f_type == "select":
                sel = html.SELECT(Id=f_id, Class=base_input)
                if ph: sel <= html.OPTION(ph, value="")
                for opt in f.get("options", []):
                    # opt peut être "Value" ou ("value", "Label")
                    val = opt[0] if isinstance(opt, tuple) else opt
                    txt = opt[1] if isinstance(opt, tuple) else opt
                    sel <= html.OPTION(txt, value=val)
                wrapper <= sel
                
            elif f_type == "checkboxes":
                fieldset = html.FIELDSET()
                fieldset <= html.LEGEND(label_text, Class=f"block text-sm font-medium {t['text_main']}")
                div_checks = html.DIV(Class="mt-2 space-y-2")
                
                for opt in f.get("options", []):
                    val = opt[0] if isinstance(opt, tuple) else opt
                    txt = opt[1] if isinstance(opt, tuple) else opt
                    cid = f"{f_id}-{val}"
                    
                    row = html.DIV(Class="flex items-center gap-2")
                    row <= html.INPUT(
                        type="checkbox", Id=cid, name=f_id, value=val,
                        Class=f"size-5 rounded border {t['border']} text-{t['accent']}-600 focus:ring-{t['accent']}-500 dark:bg-gray-900"
                    )
                    row <= html.LABEL(txt, For=cid, Class=f"text-sm {t['text_main']}")
                    div_checks <= row
                
                fieldset <= div_checks
                wrapper <= fieldset
                
            else: # text, email, tel
                wrapper <= html.INPUT(type=f_type, Id=f_id, placeholder=ph, Class=base_input)
                
            return wrapper

        # --- Construction du Formulaire ---
        
        # Styles du conteneur form
        form_cls = f"rounded-lg border {t['border']} bg-gray-100 p-6 dark:bg-gray-800 space-y-4"
        if layout == "grid":
            form_cls = form_cls.replace("space-y-4", "grid grid-cols-1 gap-4 sm:grid-cols-2")
            
        form = html.FORM(action="#", Class=form_cls)
        
        # Génération des champs
        for field in fields:
            form <= render_field(field)
            
        # Bouton Submit
        # Dans une grid, le bouton prend souvent toute la largeur
        btn_wrapper_cls = "md:col-span-2" if layout == "grid" else ""
        btn_wrapper = html.DIV(Class=btn_wrapper_cls)
        
        submit_btn = html.BUTTON(
            "Send Message", 
            type="submit",
            Class=f"block w-full rounded-lg bg-{t['accent']}-600 px-12 py-3 text-sm font-medium text-white transition-colors hover:bg-{t['accent']}-700 focus:outline-none focus:ring active:bg-{t['accent']}-500"
        )
        
        # Gestion du Submit
        def _handle_submit(ev):
            ev.preventDefault()
            if on_submit:
                # Récupération basique des données (pour l'exemple)
                # Une vraie implémentation utiliserait FormData
                on_submit("Form submitted!")
        
        form.bind("submit", _handle_submit)
        
        btn_wrapper <= submit_btn
        form <= btn_wrapper

        # --- Layout Split (Side-by-Side) ---
        if layout == "split" and contact_details:
            container = html.DIV(Class=f"grid grid-cols-1 gap-8 md:grid-cols-2 {extra_class}")
            
            # Bloc Info (Gauche)
            info = html.DIV(Class="md:py-4")
            info <= html.H2("Get in touch", Class=f"text-2xl font-bold {t['text_main']} sm:text-3xl")
            info <= html.P("Lorem ipsum dolor sit amet...", Class=f"mt-4 text-pretty {t['text_muted']}")
            
            dl = html.DL(Class="mt-6 space-y-3")
            
            # Helper pour ligne de contact
            def info_row(icon_path, text):
                div = html.DIV()
                dd = html.DD(Class=f"grid grid-cols-[24px_1fr] items-center gap-2 {t['text_muted']}")
                svg = html.SVG(xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke_width="1.5", stroke="currentColor", Class="size-5")
                svg <= html.PATH(stroke_linecap="round", stroke_linejoin="round", d=icon_path)
                dd <= svg
                dd <= html.SPAN(text, Class="font-medium")
                div <= dd
                return div

            if "phone" in contact_details:
                dl <= info_row("M10.5 1.5H8.25A2.25 2.25 0 0 0 6 3.75v16.5a2.25 2.25 0 0 0 2.25 2.25h7.5A2.25 2.25 0 0 0 18 20.25V3.75a2.25 2.25 0 0 0-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3", contact_details["phone"])
            if "email" in contact_details:
                dl <= info_row("M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75", contact_details["email"])
            if "address" in contact_details:
                dl <= info_row("m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25", contact_details["address"])
                
            info <= dl
            
            container <= info
            container <= form
            return container

        # Layout Simple ou Grid (retourne juste le form)
        return form

    # ==========================================
    # 42. COMPOSANTS MARKETING (CTA)
    # ==========================================

    @staticmethod
    def CTA(title, description, button=None, image=None, images=None, form=None, variant="split", extra_class=""):
        """
        Section d'appel à l'action (Call To Action).
        
        Args:
            title: Titre principal.
            description: Texte descriptif.
            button: Dict {'text': 'Start', 'url': '#'} (pour split/offset/grid).
            image: URL d'image unique (pour split/offset).
            images: Liste d'URLs d'images (pour variant 'grid').
            form: Dict {'placeholder': 'Email', 'btn_text': 'Sign Up'} (pour variant 'newsletter').
            variant: "split" (std), "offset" (image arrondie), "newsletter" (centré + input), "grid" (bloc couleur).
        """
        t = UI.THEME
        
        # Fond de section général (sauf pour grid qui gère son propre conteneur)
        bg_cls = "bg-gray-50 dark:bg-gray-900" if variant != "grid" else ""
        section = html.SECTION(Class=f"overflow-hidden {bg_cls} {extra_class}")
        
        # --- VARIANT 1: NEWSLETTER (Centré) ---
        if variant == "newsletter":
            wrapper = html.DIV(Class="p-8 md:p-12 lg:px-16 lg:py-24")
            content = html.DIV(Class="mx-auto max-w-lg text-center")
            
            content <= html.H2(title, Class=f"text-2xl font-bold {t['text_main']} md:text-3xl")
            if description:
                content <= html.P(description, Class=f"hidden {t['text_muted']} sm:mt-4 sm:block")
            
            wrapper <= content
            
            # Formulaire
            if form:
                form_div = html.DIV(Class="mx-auto mt-8 max-w-xl")
                form_tag = html.FORM(action="#", Class="sm:flex sm:gap-4")
                
                # Input
                input_div = html.DIV(Class="sm:flex-1")
                input_div <= html.LABEL("Email", For="email", Class="sr-only")
                input_div <= html.INPUT(
                    type="email", 
                    placeholder=form.get("placeholder", "Email address"),
                    Class=f"w-full rounded-md border {t['border']} {t['input_bg']} {t['text_main']} p-3 shadow-sm transition focus:ring-2 focus:ring-{t['accent']}-400 focus:outline-none"
                )
                
                # Bouton
                btn = html.BUTTON(
                    type="submit",
                    Class=f"group mt-4 flex w-full items-center justify-center gap-2 rounded-md bg-{t['accent']}-600 px-5 py-3 text-white transition focus:ring-2 focus:ring-{t['accent']}-400 focus:outline-none sm:mt-0 sm:w-auto"
                )
                btn <= html.SPAN(form.get("btn_text", "Sign Up"), Class="text-sm font-medium")
                btn <= UI.Icon("arrow-right", size=16, extra_class="rtl:rotate-180") # Fleche
                
                form_tag <= input_div
                form_tag <= btn
                form_div <= form_tag
                wrapper <= form_div
                
            section <= wrapper
            return section

        # --- VARIANT 2, 3, 4: SPLIT / OFFSET / GRID ---
        
        # Configuration Layout
        if variant == "grid":
            # Layout Grid specifique (Conteneur large)
            container = html.DIV(Class="mx-auto max-w-screen-2xl px-4 py-8 sm:px-6 lg:px-8")
            grid_wrapper = html.DIV(Class="grid grid-cols-1 gap-4 md:grid-cols-2")
        else:
            # Layout Split standard (Section devient la grid)
            section.classList.add("sm:grid", "sm:grid-cols-2", "sm:items-center")
            
        # 1. Contenu Texte
        if variant == "grid":
            # Bloc coloré (Bleu par défaut)
            txt_div = html.DIV(Class=f"bg-{t['accent']}-600 p-8 md:p-12 lg:px-16 lg:py-24")
            h_color = "text-white"
            p_color = "text-white/90"
        else:
            # Bloc standard transparent
            txt_div = html.DIV(Class="p-8 md:p-12 lg:px-16 lg:py-24")
            h_color = f"{t['text_main']}"
            p_color = f"{t['text_muted']}"

        inner_txt = html.DIV(Class="mx-auto max-w-xl text-center ltr:sm:text-left rtl:sm:text-right")
        inner_txt <= html.H2(title, Class=f"text-2xl font-bold {h_color} md:text-3xl")
        
        if description:
            inner_txt <= html.P(description, Class=f"hidden {p_color} md:mt-4 md:block")
            
        if button:
            mt = "mt-4 md:mt-8"
            if variant == "grid":
                # Bouton blanc sur fond bleu
                btn_cls = f"inline-block rounded border border-white bg-white px-12 py-3 text-sm font-medium text-{t['accent']}-600 transition hover:bg-transparent hover:text-white focus:ring-2 focus:ring-white"
            else:
                # Bouton standard
                btn_cls = f"inline-block rounded bg-{t['accent']}-600 px-12 py-3 text-sm font-medium text-white transition hover:bg-{t['accent']}-700 focus:ring-2 focus:ring-{t['accent']}-400"
            
            btn_el = html.A(button.get("text", "Action"), href=button.get("url", "#"), Class=btn_cls)
            inner_txt <= html.DIV(btn_el, Class=mt)
            
        txt_div <= inner_txt

        # 2. Partie Visuelle (Image ou Grille d'images)
        if variant == "grid" and images:
            # Grille d'images
            visual_div = html.DIV(Class="grid grid-cols-2 gap-4 md:grid-cols-1 lg:grid-cols-2")
            for img_src in images:
                visual_div <= html.IMG(src=img_src, alt="", Class="h-40 w-full object-cover sm:h-56 md:h-full")
        else:
            # Image unique (Split / Offset)
            img_cls = "h-full w-full object-cover"
            if variant == "offset":
                # Style arrondi spécifique
                img_cls += " sm:h-[calc(100%-2rem)] sm:self-end sm:rounded-ss-[30px] md:h-[calc(100%-4rem)] md:rounded-ss-[60px]"
            elif variant != "grid":
                # Split standard
                img_cls += " sm:h-full"
                
            visual_div = html.IMG(src=image, alt="", Class=img_cls) if image else html.DIV()

        # Assemblage final
        if variant == "grid":
            grid_wrapper <= txt_div
            grid_wrapper <= visual_div
            container <= grid_wrapper
            section <= container
        else:
            section <= txt_div
            section <= visual_div
            
        return section

    # ==========================================
    # 43. COMPOSANTS DE FEEDBACK (EMPTY STATE)
    # ==========================================

    @staticmethod
    def EmptyState(title, description, icon=None, actions=None, form=None, footer=None, extra_class=""):
        """
        Composant pour état vide (0 résultats, 404, Panier vide).
        
        Args:
            title: Titre principal.
            description: Texte explicatif.
            icon: Path SVG (str) ou Élément SVG. Affiché en grand (size-20).
            actions: Liste de dicts [{'text': 'Retour', 'href': '#', 'variant': 'primary'}].
            form: Dict pour un formulaire simple (Coming Soon) {'placeholder': 'Email', 'btn_text': 'Notify'}.
            footer: Élément ou texte à afficher tout en bas.
        """
        t = UI.THEME
        
        container = html.DIV(Class=f"max-w-md mx-auto text-center {extra_class}")
        
        # 1. Grande Icône
        if icon:
            if isinstance(icon, str):
                svg = html.SVG(xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke_width="1.5", stroke="currentColor", Class=f"mx-auto size-20 text-gray-400 dark:text-gray-500")
                svg <= html.PATH(stroke_linecap="round", stroke_linejoin="round", d=icon)
                container <= svg
            else:
                icon.classList.add("mx-auto", "size-20", "text-gray-400", "dark:text-gray-500")
                container <= icon
                
        # 2. Titre & Description
        container <= html.H2(title, Class=f"mt-6 text-2xl font-bold {t['text_main']}")
        container <= html.P(description, Class=f"mt-4 text-pretty {t['text_muted']}")
        
        # 3. Actions (Boutons empilés)
        if actions:
            btns_div = html.DIV(Class="mt-6 space-y-2")
            for act in actions:
                is_primary = act.get("variant") == "primary"
                
                # Styles (similaires aux boutons CTA)
                if is_primary:
                    b_cls = f"block w-full rounded-lg bg-{t['accent']}-600 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-{t['accent']}-700"
                else:
                    b_cls = f"block w-full rounded-lg border {t['border']} px-6 py-3 text-sm font-medium {t['text_main']} transition-colors hover:{t['hover']}"
                
                # Tag A ou Button
                if act.get("onclick"):
                    btn = html.BUTTON(act["text"], type="button", Class=b_cls)
                    btn.bind("click", act["onclick"])
                else:
                    btn = html.A(act["text"], href=act.get("href", "#"), Class=b_cls)
                    
                btns_div <= btn
            container <= btns_div
            
        # 4. Formulaire (Alternative aux actions)
        if form:
            form_tag = html.FORM(Class="mt-6 space-y-2")
            
            inp = html.INPUT(
                type="email", 
                placeholder=form.get("placeholder", "your@email.com"),
                Class=f"w-full rounded-lg border {t['border']} {t['input_bg']} {t['text_main']} px-4 py-3 text-sm focus:border-{t['accent']}-500 focus:outline-none focus:ring-1 focus:ring-{t['accent']}-500"
            )
            
            btn = html.BUTTON(
                form.get("btn_text", "Submit"),
                Class=f"block w-full rounded-lg bg-{t['accent']}-600 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-{t['accent']}-700"
            )
            def _submit_fake(e):
                e.preventDefault()
                btn.text = "Sent!"
                
            form_tag.bind("submit", _submit_fake)
            form_tag <= inp
            form_tag <= btn
            container <= form_tag
            
        # 5. Footer (Links text)
        if footer:
            footer_div = html.DIV(Class=f"mt-6 text-sm {t['text_muted']}")
            if isinstance(footer, str):
                footer_div.text = footer
            else:
                footer_div <= footer
            container <= footer_div
            
        return container

    # ==========================================
    # 44. COMPOSANTS DE CONTENU (FAQ)
    # ==========================================

    @staticmethod
    def FAQ(items, variant="base", exclusive=False, extra_class=""):
        """
        Liste de questions/réponses (Accordéon).
        
        Args:
            items: Liste de dicts [{'question': '...', 'answer': '...'}].
            variant: "base" (blocs séparés), "divided" (liste continue), "background" (bordure latérale).
            exclusive: Si True, une seule question ouverte à la fois.
        """
        t = UI.THEME
        
        # ID de groupe pour le mode exclusif (attribut 'name' sur details)
        group_name = f"faq-group-{int(window.Math.random()*10000)}" if exclusive else None
        
        # Conteneur principal
        container_cls = extra_class
        if variant == "divided":
            container_cls += f" flow-root"
            # Wrapper interne pour la division
            wrapper_cls = f"-my-4 divide-y {t['border'].replace('border-', 'divide-')}"
            wrapper = html.DIV(Class=wrapper_cls)
            container = html.DIV(Class=container_cls)
            container <= wrapper
            target_parent = wrapper
        else:
            container_cls += " space-y-4"
            container = html.DIV(Class=container_cls)
            target_parent = container

        for item in items:
            question = item.get("question", "Question ?")
            answer = item.get("answer", "Réponse...")
            
            # --- DETAILS ---
            details_attrs = {"name": group_name} if group_name else {}
            details = html.DETAILS(Class="group [&_summary::-webkit-details-marker]:hidden", **details_attrs)
            
            # --- SUMMARY (Titre) ---
            sum_cls = "flex cursor-pointer items-center justify-between gap-1.5 text-gray-900 dark:text-white"
            
            if variant == "base":
                sum_cls += f" rounded-lg border {t['border']} {t['panel_bg']} p-4"
            elif variant == "background":
                sum_cls += f" border-s-4 border-{t['accent']}-600 {t['panel_bg']} p-4"
            elif variant == "divided":
                sum_cls += " py-4" # Juste padding vertical
                
            summary = html.SUMMARY(Class=sum_cls)
            
            summary <= html.H2(question, Class="text-lg font-medium")
            
            # Icône Chevron qui tourne
            icon = UI.Icon("M19 9l-7 7-7-7", size=20)
            icon.classList.add("shrink-0", "transition-transform", "duration-300", "group-open:-rotate-180")
            summary <= icon
            
            # --- CONTENT (Réponse) ---
            p_cls = f"leading-relaxed {t['text_muted']}"
            if variant == "divided":
                p_cls += " pb-4"
            else:
                p_cls += " mt-4 px-4"
                
            content = html.P(answer, Class=p_cls)
            
            details <= summary
            details <= content
            target_parent <= details
            
        return container


    # ==========================================
    # 45. COMPOSANTS DE NAVIGATION (FOOTER)
    # ==========================================

    @staticmethod
    def Footer(columns=None, brand_content=None, newsletter=None, social_links=None, copyright="© 2025 All rights reserved.", variant="large", extra_class=""):
        """
        Pied de page complet.
        
        Args:
            columns: Liste de dicts [{'title': 'Services', 'links': [('Link 1', '#'), ...]}].
            brand_content: Élément ou texte pour la zone marque (Logo + Desc).
            newsletter: Dict {'title': '...', 'desc': '...', 'placeholder': '...'} (pour variant large).
            social_links: Liste de dicts [{'icon': 'twitter', 'href': '#'}].
            variant: "large" (Newsletter + Cols), "simple" (Centré/Row), "split" (Image/Contenu).
        """
        t = UI.THEME
        
        footer = html.FOOTER(Class=f"{t['panel_bg']} border-t {t['border']} {extra_class}")
        container = html.DIV(Class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8")
        
        # --- VARIANT 1: LARGE (Newsletter + Colonnes) ---
        if variant == "large":
            # Partie Haute (Newsletter + Marque)
            if newsletter or brand_content:
                top_grid = html.DIV(Class="xl:grid xl:grid-cols-3 xl:gap-8")
                
                # Marque + Social (Col Gauche)
                brand_col = html.DIV(Class="space-y-8 xl:col-span-1")
                if brand_content:
                    if isinstance(brand_content, str):
                        brand_col <= html.P(brand_content, Class=f"{t['text_muted']} text-sm")
                    else:
                        brand_col <= brand_content
                        
                if social_links:
                    social_div = html.DIV(Class="flex gap-6")
                    for s in social_links:
                        a = html.A(href=s.get("href", "#"), Class=f"{t['text_muted']} hover:{t['text_main']} transition")
                        a <= UI.Icon(s.get("icon", "link"), size=24) # size-6
                        social_div <= a
                    brand_col <= social_div
                    
                top_grid <= brand_col
                
                # Colonnes de liens (Col Droite - Grid imbriquée)
                if columns:
                    links_grid = html.DIV(Class="mt-16 grid grid-cols-2 gap-8 xl:col-span-2 xl:mt-0")
                    # On divise les colonnes en 2 groupes pour le responsive si beaucoup de colonnes
                    # Simplification : grid-cols-2 ou 4 selon le nombre
                    cols_count = len(columns)
                    links_grid.class_name += f" md:grid-cols-{min(cols_count, 4)}"
                    
                    for col in columns:
                        div = html.DIV()
                        div <= html.H3(col.get("title", ""), Class=f"text-sm font-semibold {t['text_main']} tracking-wider uppercase")
                        ul = html.UL(Class="mt-4 space-y-4")
                        for link_txt, link_url in col.get("links", []):
                            li = html.LI()
                            li <= html.A(link_txt, href=link_url, Class=f"text-base {t['text_muted']} hover:{t['text_main']} transition")
                            ul <= li
                        div <= ul
                        links_grid <= div
                        
                    top_grid <= links_grid
                
                container <= top_grid
                
            # Copyright (Bas)
            if copyright:
                btm = html.DIV(Class=f"mt-12 border-t {t['border']} pt-8")
                btm <= html.P(copyright, Class=f"text-base {t['text_muted']} xl:text-center")
                container <= btm

        # --- VARIANT 2: SIMPLE (Centré) ---
        elif variant == "simple":
            # Flex Centré
            center_div = html.DIV(Class="flex flex-col items-center justify-center space-y-4 sm:flex-row sm:justify-between sm:space-y-0")
            
            # Marque
            if brand_content:
                center_div <= (html.DIV(brand_content) if not isinstance(brand_content, str) else html.SPAN(brand_content, Class=f"text-lg font-bold {t['text_main']}"))
                
            # Copyright
            if copyright:
                center_div <= html.P(copyright, Class=f"text-sm {t['text_muted']}")
                
            container <= center_div
            
        footer <= container
        return footer        

    
    # ==========================================
    # 46. COMPOSANTS DE NAVIGATION (HEADER)
    # ==========================================

    @staticmethod
    def Header(logo, links=None, actions=None, user_info=None, on_mobile_click=None, extra_class=""):
        """
        En-tête de navigation responsive.
        
        Args:
            logo: Texte (str) ou Élément HTML/SVG.
            links: Liste de tuples [('Home', '#'), ('About', '#')] ou dicts.
            actions: Liste de boutons [{'text': 'Login', 'variant': 'primary', 'href': '/login'}].
            user_info: Dict {'name': 'John', 'avatar': 'url', 'menu': [('Profile', '#'), ('Logout', '#')]}
                       Si présent, remplace 'actions'.
            on_mobile_click: Callback pour le bouton hamburger mobile.
        """
        t = UI.THEME
        
        # Structure de base
        header = html.HEADER(Class=f"{t['panel_bg']} border-b {t['border']} {extra_class}")
        container = html.DIV(Class="mx-auto flex h-16 max-w-7xl items-center gap-8 px-4 sm:px-6 lg:px-8")
        
        # --- 1. Logo ---
        logo_link = html.A(href="#", Class=f"block text-{t['accent']}-600")
        if isinstance(logo, str):
            # Si c'est juste du texte, on le met en gras, sinon on assume que c'est un path SVG
            if logo.strip().startswith("<") or " " in logo.strip() or len(logo) < 100: # Heuristique simple
                logo_link <= html.SPAN(logo, Class="text-xl font-bold")
            else:
                 # C'est probablement un path SVG envoyé comme string (ex: les icones HyperUI)
                 logo_link <= UI.Icon(logo, size=32)
        else:
            logo_link <= logo
            
        container <= logo_link
        
        # --- 2. Navigation (Desktop) ---
        # Flex-1 pour pousser le reste à droite
        nav_wrapper = html.DIV(Class="hidden md:flex md:flex-1 md:items-center md:justify-between")
        
        # Liens
        nav = html.NAV(aria_label="Global")
        ul = html.UL(Class="flex items-center gap-6 text-sm")
        
        if links:
            for link in links:
                # Support tuple ou dict
                txt = link[0] if isinstance(link, tuple) else link.get("text")
                url = link[1] if isinstance(link, tuple) else link.get("href", "#")
                
                li = html.LI()
                a = html.A(
                    txt, 
                    href=url, 
                    Class=f"{t['text_muted']} transition hover:{t['text_main']} hover:underline underline-offset-4"
                )
                li <= a
                ul <= li
        nav <= ul
        nav_wrapper <= nav
        
        # --- 3. Actions / User Menu (Desktop) ---
        right_area = html.DIV(Class="flex items-center gap-4")
        
        # Mode Utilisateur Connecté (Avatar + Dropdown)
        if user_info:
            # Wrapper relatif pour le dropdown
            user_div = html.DIV(Class="relative")
            
            # Avatar Button
            avatar_btn = html.BUTTON(
                type="button",
                Class=f"overflow-hidden rounded-full border {t['border']} shadow-inner transition hover:opacity-75 focus:outline-none focus:ring"
            )
            
            avatar_url = user_info.get("avatar")
            if avatar_url:
                avatar_btn <= html.IMG(src=avatar_url, alt=user_info.get("name", "User"), Class="size-10 object-cover")
            else:
                # Placeholder
                avatar_btn <= html.DIV(
                    user_info.get("name", "U")[:1].upper(), 
                    Class=f"size-10 grid place-content-center bg-{t['accent']}-100 text-{t['accent']}-700 font-bold"
                )
                
            user_div <= avatar_btn
            
            # Menu Dropdown (Caché par défaut)
            menu_items = user_info.get("menu", [])
            if menu_items:
                dropdown = html.DIV(
                    Class=f"hidden absolute end-0 z-10 mt-2 w-56 rounded-md border {t['border']} {t['panel_bg']} shadow-lg",
                    role="menu"
                )
                div_p = html.DIV(Class="p-2")
                for m_txt, m_action in menu_items:
                    # m_action peut être une URL (str) ou une fonction (callback)
                    if callable(m_action):
                        m_el = html.BUTTON(m_txt, Class=f"block w-full text-left rounded-lg px-4 py-2 text-sm {t['text_muted']} hover:{t['hover']} hover:{t['text_main']}")
                        m_el.bind("click", m_action)
                    else:
                        m_el = html.A(m_txt, href=m_action, Class=f"block rounded-lg px-4 py-2 text-sm {t['text_muted']} hover:{t['hover']} hover:{t['text_main']}")
                    div_p <= m_el
                
                dropdown <= div_p
                user_div <= dropdown
                
                # Toggle Logic
                def toggle_user_menu(ev):
                    ev.stopPropagation()
                    if dropdown.classList.contains("hidden"):
                        dropdown.classList.remove("hidden")
                    else:
                        dropdown.classList.add("hidden")
                
                # Fermer si on clique ailleurs
                def close_user_menu(ev):
                    if not dropdown.classList.contains("hidden"):
                        dropdown.classList.add("hidden")
                        
                avatar_btn.bind("click", toggle_user_menu)
                document.bind("click", close_user_menu)

            right_area <= user_div
            
        # Mode Visiteur (Boutons Login/Register)
        elif actions:
            btns_grp = html.DIV(Class="sm:flex sm:gap-4")
            for act in actions:
                is_primary = act.get("variant") == "primary"
                b_cls = f"rounded-md px-5 py-2.5 text-sm font-medium transition shadow-sm "
                if is_primary:
                    b_cls += f"bg-{t['accent']}-600 text-white hover:bg-{t['accent']}-700"
                else:
                    b_cls += f"bg-gray-100 text-{t['accent']}-600 hover:text-{t['accent']}-600/75 dark:bg-gray-800 dark:text-white dark:hover:text-white/75"
                
                btn = html.A(act["text"], href=act.get("href", "#"), Class=b_cls)
                btns_grp <= btn
            right_area <= btns_grp
            
        nav_wrapper <= right_area
        container <= nav_wrapper
        
        # --- 4. Mobile Menu Button ---
        mobile_btn = html.BUTTON(
            Class=f"block rounded bg-gray-100 p-2.5 text-gray-600 transition hover:text-gray-600/75 md:hidden dark:bg-gray-800 dark:text-white dark:hover:text-white/75"
        )
        mobile_btn <= UI.Icon("menu", size=20)
        
        if on_mobile_click:
            mobile_btn.bind("click", on_mobile_click)
            
        container <= mobile_btn
        
        header <= container
        return header
    

    # ==========================================
    # 47. COMPOSANTS MARKETING (LOGO CLOUD)
    # ==========================================

    @staticmethod
    def LogoCloud(logos, title=None, text=None, variant="base", extra_class=""):
        """
        Grille de logos partenaires.
        
        Args:
            logos: Liste de logos (Strings SVG paths ou URLs d'images).
            title: Titre de la section (optionnel).
            text: Description (optionnel).
            variant: "base" (simple), "grid-lines" (bordures entre logos).
        """
        t = UI.THEME
        
        section = html.DIV(Class=f"mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 {extra_class}")
        
        # En-tête (Titre + Texte)
        if title or text:
            header = html.DIV(Class="mx-auto max-w-lg text-center mb-8")
            if title:
                header <= html.H2(title, Class=f"text-2xl font-bold {t['text_main']} sm:text-3xl")
            if text:
                header <= html.P(text, Class=f"mt-4 text-pretty {t['text_muted']}")
            section <= header
            
        # Grille des Logos
        if variant == "grid-lines":
            # Style "Tableau" avec bordures
            # Astuce Tailwind: gap-px + bg-gray-200 sur le parent + bg-white sur les enfants crée les bordures
            grid_cls = f"grid grid-cols-2 gap-px overflow-hidden rounded-lg bg-gray-200 dark:bg-gray-700 md:grid-cols-4"
            item_bg = f"bg-white dark:bg-gray-900"
        else:
            # Style Simple
            grid_cls = "grid grid-cols-2 gap-8 md:grid-cols-4"
            item_bg = ""

        grid = html.DIV(Class=grid_cls)
        
        for logo_data in logos:
            # Wrapper Logo
            wrapper = html.DIV(Class=f"grid place-content-center p-4 {item_bg} grayscale transition-[filter] hover:grayscale-0")
            
            if logo_data.strip().startswith("<") or " " in logo_data.strip():
                # SVG Path ou SVG complet
                if logo_data.strip().startswith("<svg"):
                    # SVG complet passé en string
                    # Brython ne parse pas le SVG string directement en DOM facile -> innerHTML
                    tmp = html.DIV()
                    tmp.innerHTML = logo_data
                    svg = tmp.firstChild
                    svg.classList.add("h-8")
                    wrapper <= svg
                else:
                    # Juste le path
                    svg = html.SVG(xmlns="http://www.w3.org/2000/svg", fill="currentColor", viewBox="0 0 285 40", Class=f"h-8 {t['text_main']}")
                    svg <= html.PATH(d=logo_data)
                    wrapper <= svg
            else:
                # URL Image
                wrapper <= html.IMG(src=logo_data, alt="Logo", Class="h-8 object-contain")
                
            grid <= wrapper
            
        section <= grid
        return section
    

    # ==========================================
    # 48. COMPOSANTS MARKETING (NEWSLETTER)
    # ==========================================

    @staticmethod
    def Newsletter(title, description, placeholder="Enter your email", button_text="Sign Up", variant="simple", on_submit=None, extra_class=""):
        """
        Section d'inscription Newsletter.
        
        Args:
            title: Titre de la section.
            description: Texte incitatif.
            placeholder: Texte dans l'input email.
            button_text: Texte du bouton.
            variant: "simple" (gauche) ou "centered" (centré).
            on_submit: Callback (reçoit l'email).
        """
        t = UI.THEME
        
        # Conteneur principal (Fond contrasté par défaut pour ressortir)
        container = html.DIV(Class=f"bg-gray-100 dark:bg-gray-800 {extra_class}")
        wrapper = html.DIV(Class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8")
        
        # --- 1. Contenu Texte ---
        # Gestion de l'alignement
        text_cls = "max-w-prose"
        if variant == "centered":
            text_cls = "mx-auto max-w-prose text-center"
            
        content = html.DIV(Class=text_cls)
        content <= html.H2(title, Class=f"text-2xl font-bold {t['text_main']} sm:text-3xl")
        content <= html.P(description, Class=f"mt-4 text-pretty {t['text_muted']}")
        
        wrapper <= content
        
        # --- 2. Formulaire ---
        form_cls = "mt-6 flex max-w-xl flex-col gap-4 sm:flex-row sm:items-center"
        if variant == "centered":
            form_cls += " mx-auto sm:justify-center"
            
        form = html.FORM(action="#", Class=form_cls)
        
        # Input Wrapper (Label caché + Input)
        # Flex-1 pour prendre la place dispo
        label_wrap = html.LABEL(For="email_nl", Class="flex-1")
        label_wrap <= html.SPAN("Email", Class="sr-only")
        
        inp = html.INPUT(
            type="email", 
            Id="email_nl", 
            placeholder=placeholder,
            Class=f"h-12 w-full rounded border {t['border']} {t['input_bg']} {t['text_main']} px-4 shadow-sm focus:ring-{t['accent']}-500 focus:border-{t['accent']}-500 focus:outline-none"
        )
        label_wrap <= inp
        form <= label_wrap
        
        # Bouton
        btn = html.BUTTON(
            button_text,
            type="submit",
            Class=f"h-12 rounded bg-{t['accent']}-600 px-8 py-3 text-sm font-medium text-white transition hover:bg-{t['accent']}-700 focus:outline-none focus:ring"
        )
        form <= btn
        
        # Gestion Submit
        def _handle_submit(ev):
            ev.preventDefault()
            if on_submit: on_submit(inp.value)
            
        form.bind("submit", _handle_submit)
        
        wrapper <= form
        container <= wrapper
        
        return container
    

    # ==========================================
    # 49. COMPOSANTS D'ENGAGEMENT (POLL)
    # ==========================================

    @staticmethod
    def Poll(question, options, description=None, multiple=False, end_date=None, name_id="poll", extra_class=""):
        """
        Sondage interactif avec visualisation des résultats.
        
        Args:
            question: La question posée.
            options: Liste de dicts [{'label': 'Option A', 'percent': 45, 'value': 'a'}].
            description: Texte d'aide.
            multiple: Si True, utilise des Checkbox, sinon Radio.
            end_date: Texte de fin (ex: "Ends on Oct 31").
            name_id: Identifiant unique pour le groupe d'inputs.
        """
        t = UI.THEME
        
        container = html.DIV(Class=f"mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 {extra_class}")
        
        # En-tête
        header = html.DIV(Class="max-w-prose")
        header <= html.H2(question, Class=f"text-2xl font-semibold {t['text_main']} sm:text-3xl")
        if description:
            header <= html.P(description, Class=f"mt-4 text-pretty {t['text_muted']}")
            
        container <= header
        
        # Formulaire
        form = html.FORM(action="#", Class="mt-6 space-y-4")
        fieldset = html.FIELDSET(Class="space-y-4")
        fieldset <= html.LEGEND("Select an option", Class="sr-only")
        
        input_type = "checkbox" if multiple else "radio"
        
        for i, opt in enumerate(options):
            label_txt = opt.get("label", "")
            percent = opt.get("percent", 0)
            val = opt.get("value", label_txt)
            opt_id = f"{name_id}_opt_{i}"
            
            # Ligne Flex
            row = html.DIV(Class="flex items-center gap-4")
            
            # Label (Le gros bloc cliquable avec la barre de progression)
            # overflow-hidden est important pour que la barre de fond ne dépasse pas
            label_block = html.LABEL(
                For=opt_id, 
                Class=f"relative block flex-1 overflow-hidden rounded border {t['border']} px-4 py-2 shadow-sm cursor-pointer hover:{t['hover']}"
            )
            
            # Barre de progression (Background)
            # On utilise un gris clair pour simuler le remplissage
            bar_bg = html.DIV(
                style={"width": f"{percent}%"},
                Class="absolute inset-y-0 left-0 bg-gray-100 dark:bg-gray-800 transition-all duration-500"
            )
            label_block <= bar_bg
            
            # Contenu (Input + Texte) au-dessus de la barre
            content = html.DIV(Class="relative flex items-center gap-4")
            
            inp = html.INPUT(
                type=input_type, 
                Id=opt_id, 
                name=name_id, 
                value=val,
                Class=f"size-5 border-gray-300 shadow-sm focus:ring-{t['accent']}-500 text-{t['accent']}-600 dark:bg-gray-900 dark:border-gray-600"
            )
            content <= inp
            content <= html.SPAN(label_txt, Class=f"font-medium {t['text_main']}")
            
            label_block <= content
            row <= label_block
            
            # Pourcentage affiché à droite
            row <= html.SPAN(f"{percent}%", Class=f"{t['text_muted']}")
            
            fieldset <= row
            
        form <= fieldset
        container <= form
        
        # Footer Date
        if end_date:
            container <= html.P(f"Ends on {end_date}", Class=f"mt-4 text-sm {t['text_muted']}")
            
        return container
    
    # ==========================================
    # 48. COMPOSANTS MARKETING (PRICING)
    # ==========================================

    @staticmethod
    def Pricing(plans, extra_class=""):
        """
        Tableaux de prix (Pricing Tables).
        
        Args:
            plans: Liste de dicts définissant chaque offre.
                   Exemple:
                   {
                       'name': 'Pro',
                       'price': '30$',
                       'period': 'month',
                       'description': 'Pour les pros.',
                       'features': ['20 users', '5GB storage'],
                       'highlight': True, # Met en avant cette carte
                       'button_text': 'Get Started',
                       'action': callback ou url
                   }
        """
        t = UI.THEME
        
        container = html.DIV(Class=f"mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-12 lg:px-8 {extra_class}")
        
        # Configuration de la grille selon le nombre de plans
        cols = len(plans)
        grid_cls = f"grid grid-cols-1 gap-4 sm:grid-cols-2 md:gap-8 lg:grid-cols-{min(cols, 3)}"
        if cols == 2:
            grid_cls += " sm:items-center" # Centre verticalement si 2 cartes dont une highlight
        elif cols >= 3:
            grid_cls += " sm:items-stretch"
            
        grid = html.DIV(Class=grid_cls)
        
        for plan in plans:
            is_highlight = plan.get("highlight", False)
            
            # --- Styles de la Carte ---
            if is_highlight:
                # Bordure colorée + Ombre + Ring
                card_cls = (
                    f"rounded-2xl border border-{t['accent']}-600 p-6 shadow-sm ring-1 ring-{t['accent']}-600 "
                    f"sm:px-8 lg:p-12 {t['panel_bg']} sm:order-last" # order-last sur mobile souvent pour le focus
                )
                # Bouton plein
                btn_cls = (
                    f"mt-8 block w-full rounded-full border border-{t['accent']}-600 bg-{t['accent']}-600 "
                    f"px-12 py-3 text-center text-sm font-medium text-white hover:bg-{t['accent']}-700 "
                    f"hover:ring-1 hover:ring-{t['accent']}-700 focus:outline-none focus:ring transition-colors"
                )
            else:
                # Bordure grise standard
                card_cls = f"rounded-2xl border {t['border']} p-6 shadow-sm sm:px-8 lg:p-12 {t['panel_bg']}"
                # Bouton outline
                btn_cls = (
                    f"mt-8 block w-full rounded-full border border-{t['accent']}-600 bg-transparent "
                    f"px-12 py-3 text-center text-sm font-medium text-{t['accent']}-600 "
                    f"hover:ring-1 hover:ring-{t['accent']}-600 focus:outline-none focus:ring transition-colors"
                )

            card = html.DIV(Class=card_cls)
            
            # --- En-tête ---
            header = html.DIV(Class="text-center")
            header <= html.H2(plan.get("name", "Plan"), Class=f"text-lg font-medium {t['text_main']}")
            
            if plan.get("description"):
                header <= html.P(plan["description"], Class=f"mt-2 text-sm {t['text_muted']}")
                
            price_block = html.P(Class="mt-2 sm:mt-4")
            price_block <= html.STRONG(plan.get("price", "0$"), Class=f"text-3xl font-bold {t['text_main']} sm:text-4xl")
            
            if plan.get("period"):
                period = plan["period"] if plan["period"].startswith("/") else f"/{plan['period']}"
                price_block <= html.SPAN(period, Class=f"text-sm font-medium {t['text_muted']}")
                
            header <= price_block
            card <= header
            
            # --- Liste des fonctionnalités ---
            ul = html.UL(Class="mt-6 space-y-2")
            for feat in plan.get("features", []):
                li = html.LI(Class="flex items-center gap-1")
                
                # Checkmark SVG
                svg = html.SVG(xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke_width="1.5", stroke="currentColor", Class=f"size-5 text-{t['accent']}-700")
                svg <= html.PATH(stroke_linecap="round", stroke_linejoin="round", d="M4.5 12.75l6 6 9-13.5")
                
                li <= svg
                li <= html.SPAN(feat, Class=f"{t['text_muted']}")
                ul <= li
                
            card <= ul
            
            # --- Bouton d'action ---
            action = plan.get("action", "#")
            btn_txt = plan.get("button_text", "Get Started")
            
            if callable(action):
                btn = html.BUTTON(btn_txt, type="button", Class=btn_cls)
                btn.bind("click", action)
            else:
                btn = html.A(btn_txt, href=action, Class=btn_cls)
                
            card <= btn
            grid <= card
            
        container <= grid
        return container
    
    # ==========================================
    # 50. COMPOSANTS E-COMMERCE (PRODUCT CARD)
    # ==========================================

    @staticmethod
    def ProductCard(title, price, image, image_hover=None, description=None, colors=None, badge=None, url="#", on_add_to_cart=None, on_wishlist=None, extra_class=""):
        """
        Carte produit e-commerce complète.
        
        Args:
            title: Nom du produit.
            price: Prix (str).
            image: URL image principale.
            image_hover: URL image au survol (optionnel).
            description: Courte description (optionnel).
            colors: Liste de codes Hex ou noms de couleurs ['#000', '#FFF'].
            badge: Texte du badge (ex: 'New', '-50%').
            url: Lien de la fiche produit.
            on_add_to_cart: Callback bouton ajout panier.
            on_wishlist: Callback bouton favori.
        """
        t = UI.THEME
        
        # Conteneur principal (Lien global pour l'UX)
        # group pour gérer les effets de survol sur les enfants
        container = html.A(href=url, Class=f"group block overflow-hidden rounded-lg border {t['border']} {t['panel_bg']} {extra_class}")
        
        # --- 1. Zone Image ---
        img_wrapper_cls = "relative h-[300px] sm:h-[350px]"
        img_container = html.DIV(Class=img_wrapper_cls)
        
        # Badge
        if badge:
            badge_el = html.SPAN(
                badge, 
                Class=f"absolute top-4 left-4 z-10 rounded-full bg-{t['accent']}-600 px-3 py-1.5 text-xs font-medium text-white shadow-md"
            )
            img_container <= badge_el
            
        # Bouton Wishlist (cœur)
        if on_wishlist:
            wish_btn = html.BUTTON(
                type="button",
                Class="absolute end-4 top-4 z-10 rounded-full bg-white p-1.5 text-gray-900 transition hover:text-red-500 hover:scale-110 shadow-sm"
            )
            # Icone Coeur SVG
            svg_heart = html.SVG(xmlns="http://www.w3.org/2000/svg", fill="none", viewBox="0 0 24 24", stroke_width="1.5", stroke="currentColor", Class="size-4")
            svg_heart <= html.PATH(stroke_linecap="round", stroke_linejoin="round", d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z")
            wish_btn <= svg_heart
            
            # Gestion clic sans déclencher le lien parent
            def _wish_click(e):
                e.preventDefault()
                e.stopPropagation()
                on_wishlist(e)
                
            wish_btn.bind("click", _wish_click)
            img_container <= wish_btn

        # Images
        base_img_cls = "absolute inset-0 h-full w-full object-cover transition duration-500"
        
        if image_hover:
            # Effet Swap
            img1 = html.IMG(src=image, alt=title, Class=f"{base_img_cls} opacity-100 group-hover:opacity-0")
            img2 = html.IMG(src=image_hover, alt=title, Class=f"{base_img_cls} opacity-0 group-hover:opacity-100")
            img_container <= img1
            img_container <= img2
        else:
            # Effet Zoom simple
            img1 = html.IMG(src=image, alt=title, Class=f"{base_img_cls} group-hover:scale-105")
            img_container <= img1
            
        container <= img_container
        
        # --- 2. Zone Contenu ---
        content = html.DIV(Class="relative p-4 pt-3")
        
        # Titre
        content <= html.H3(
            title, 
            Class=f"text-sm font-medium {t['text_main']} group-hover:underline group-hover:underline-offset-4"
        )
        
        # Prix & Info
        meta_row = html.DIV(Class="mt-1.5 flex items-center justify-between")
        meta_row <= html.P(price, Class=f"tracking-wide {t['text_main']}")
        
        if colors:
            color_txt = html.P(f"{len(colors)} Colors", Class=f"text-xs tracking-wide uppercase {t['text_muted']}")
            meta_row <= color_txt
            
        content <= meta_row
        
        # Description
        if description:
            content <= html.P(description, Class=f"mt-2 text-xs {t['text_muted']} line-clamp-2")
            
        # Pastilles de couleurs (Visuel)
        if colors:
            swatches = html.DIV(Class="mt-3 flex flex-wrap gap-1")
            for c in colors:
                swatch = html.SPAN(
                    Class="block size-4 rounded-full shadow-sm ring-1 ring-gray-200 dark:ring-gray-700", 
                    style={"background-color": c}
                )
                swatches <= swatch
            content <= swatches

        # Bouton "Add to Cart"
        if on_add_to_cart:
            btn_cart = html.BUTTON(
                "Add to Cart",
                type="button",
                Class=f"mt-4 block w-full rounded bg-{t['accent']}-600 p-3 text-sm font-medium text-white transition hover:scale-105 hover:bg-{t['accent']}-700"
            )
            
            def _cart_click(e):
                e.preventDefault()
                e.stopPropagation()
                on_add_to_cart(e)
                
            btn_cart.bind("click", _cart_click)
            content <= btn_cart
            
        container <= content
        
        return container


    # ==========================================
    # 51. COMPOSANTS E-COMMERCE (COLLECTIONS)
    # ==========================================

    @staticmethod
    def ProductCollection(products, title=None, description=None, variant="base", filters=None, sort_options=None, extra_class=""):
        """
        Grille de produits avec options de filtrage.
        
        Args:
            products: Liste de dicts (données pour UI.ProductCard).
            title: Titre de la collection.
            description: Description courte.
            variant: "base", "sidebar" (filtres gauche), "dropdown" (filtres haut).
            filters: Dict de filtres {'Couleur': ['Rouge', 'Bleu'], 'Taille': ['S', 'M']}.
            sort_options: Liste de str pour le tri (ex: ['Prix cro.', 'Prix décr.']).
        """
        t = UI.THEME
        
        section = html.SECTION(Class=f"{extra_class}")
        container = html.DIV(Class="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-12 lg:px-8")
        
        # --- 1. En-tête ---
        header = html.HEADER(Class="text-center" if variant == "base" else "")
        if title:
            header <= html.H2(title, Class=f"text-xl font-bold {t['text_main']} sm:text-3xl")
        if description:
            desc_cls = "mx-auto mt-4 max-w-md" if variant == "base" else "mt-4 max-w-md"
            header <= html.P(description, Class=f"{desc_cls} {t['text_muted']}")
            
        container <= header
        
        # --- Helper: Création d'un groupe de filtres (Accordion) ---
        def create_filter_group(label, options, style="sidebar"):
            details = html.DETAILS(
                Class=f"group overflow-hidden rounded-sm border {t['border']} [&_summary::-webkit-details-marker]:hidden"
            )
            # Résumé (Titre)
            summary = html.SUMMARY(Class=f"flex cursor-pointer items-center justify-between gap-2 p-4 {t['text_main']} transition")
            summary <= html.SPAN(label, Class="text-sm font-medium")
            
            icon = UI.Icon("M19.5 8.25l-7.5 7.5-7.5-7.5", size=16)
            icon.classList.add("transition", "group-open:-rotate-180")
            summary <= icon
            details <= summary
            
            # Contenu (Checkboxes)
            content = html.DIV(Class=f"border-t {t['border']} {t['panel_bg']}")
            ul = html.UL(Class="space-y-1 p-4")
            
            for opt in options:
                li = html.LI()
                lbl = html.LABEL(Class="inline-flex items-center gap-2")
                chk = html.INPUT(type="checkbox", Class=f"size-5 rounded border-gray-300 {t['input_bg']}")
                lbl <= chk
                lbl <= html.SPAN(opt, Class=f"text-sm font-medium {t['text_muted']}")
                li <= lbl
                ul <= li
                
            content <= ul
            details <= content
            
            if style == "dropdown":
                # En mode dropdown, le positionnement est absolute (géré par CSS parent relatif)
                # Simplification pour Brython: On garde le style accordéon mais compact
                details.class_name += " relative"
                content.class_name += " absolute z-50 w-56 mt-1 shadow-lg rounded"
                
            return details

        # --- 2. Barre d'outils (Mode Dropdown ou Mobile Toggle) ---
        toolbar = html.DIV(Class="mt-8 sm:flex sm:items-center sm:justify-between")
        
        # Sort Options (commun à tous les modes sauf base simple)
        sort_select = None
        if sort_options:
            sort_label = html.LABEL("Sort By", For="SortBy", Class="sr-only")
            sort_select = html.SELECT(Id="SortBy", Class=f"h-10 rounded border {t['border']} {t['input_bg']} {t['text_main']} text-sm px-2")
            for opt in sort_options:
                sort_select <= html.OPTION(opt)
        
        # Logique Variant
        main_grid = html.DIV(Class="mt-4 lg:mt-8")
        
        if variant == "sidebar" and filters:
            # Layout: Grid avec Sidebar à gauche
            main_grid.class_name += " lg:grid lg:grid-cols-4 lg:items-start lg:gap-8"
            
            # Sidebar (Desktop)
            sidebar = html.DIV(Class="hidden space-y-4 lg:block")
            
            # Sort dans la sidebar ou toolbar ? HyperUI met Sort dans la sidebar top
            if sort_select:
                sort_div = html.DIV()
                sort_div <= html.LABEL("Sort By", Class=f"block text-xs font-medium {t['text_muted']}")
                sort_select.class_name = f"mt-1 w-full rounded border {t['border']} {t['input_bg']} text-sm"
                sort_div <= sort_select
                sidebar <= sort_div
                
            div_lbl = html.DIV()
            div_lbl <= html.P("Filters", Class=f"block text-xs font-medium {t['text_muted']}")
            div_filters = html.DIV(Class="mt-1 space-y-2")
            
            for key, opts in filters.items():
                div_filters <= create_filter_group(key, opts, style="sidebar")
                
            div_lbl <= div_filters
            sidebar <= div_lbl
            
            main_grid <= sidebar
            
            # Product Grid Wrapper (3 cols)
            products_col = html.DIV(Class="lg:col-span-3")
            ul_prod = html.UL(Class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3")
            products_col <= ul_prod
            main_grid <= products_col
            
            # Mobile Filter Button (visible sm, hidden lg)
            mobile_bar = html.DIV(Class="block lg:hidden mb-6")
            mobile_btn = html.BUTTON(Class=f"flex cursor-pointer items-center gap-2 border-b {t['border']} pb-1 {t['text_main']}")
            mobile_btn <= html.SPAN("Filters & Sorting", Class="text-sm font-medium")
            mobile_bar <= mobile_btn
            container <= mobile_bar # Insert avant la grid

        elif variant == "dropdown" and filters:
            # Layout: Toolbar filters + Grid full
            
            # Zone Filtres (Gauche)
            filters_wrap = html.DIV(Class="hidden sm:flex sm:gap-4")
            for key, opts in filters.items():
                # On utilise un wrapper relative pour le dropdown
                rel = html.DIV(Class="relative")
                rel <= create_filter_group(key, opts, style="dropdown")
                filters_wrap <= rel
            toolbar <= filters_wrap
            
            # Zone Sort (Droite)
            if sort_select:
                sort_div = html.DIV(Class="hidden sm:block")
                sort_div <= sort_select
                toolbar <= sort_div
                
            container <= toolbar
            
            # Grid Full
            ul_prod = html.UL(Class="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4")
            main_grid <= ul_prod

        else: # Base
            # Juste la grille
            ul_prod = html.UL(Class="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4")
            main_grid <= ul_prod

        # Remplissage des produits
        # On réutilise UI.ProductCard
        for p_data in products:
            li = html.LI()
            # On passe les données en kwargs à ProductCard
            li <= UI.ProductCard(**p_data)
            ul_prod <= li
            
        container <= main_grid
        section <= container
        
        return section
    
    # ==========================================
    # 52. COMPOSANTS DE STRUCTURE (SECTIONS)
    # ==========================================

    @staticmethod
    def Section(title, text, image=None, ratio="1/2", reverse=False, extra_class=""):
        """
        Section de contenu (Texte + Image).
        
        Args:
            title: Titre (str).
            text: Paragraphe (str).
            image: URL de l'image (str) ou Élément HTML.
            ratio: "1/2" (50/50), "1/3" (Texte 33%, Img 66%), "3/1" (Texte 66%, Img 33%), "vertical" (Stack).
            reverse: Si True, place l'image avant le texte (sur desktop).
        """
        t = UI.THEME
        
        container = html.SECTION(Class=f"{extra_class}")
        wrapper = html.DIV(Class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8")
        
        # --- Configuration de la Grille ---
        if ratio == "vertical":
            grid_cls = "space-y-4 md:space-y-8"
        else:
            # Grid par défaut avec gap
            grid_cls = "grid grid-cols-1 gap-4 md:items-center md:gap-8"
            
            if ratio == "1/2":
                grid_cls += " md:grid-cols-2"
                col_txt = ""
                col_img = ""
            elif ratio == "1/3": # Texte petit, Image grande
                grid_cls += " md:grid-cols-4"
                col_txt = "md:col-span-1"
                col_img = "md:col-span-3"
            elif ratio == "3/1": # Texte grand, Image petite
                grid_cls += " md:grid-cols-4"
                col_txt = "md:col-span-3"
                col_img = "md:col-span-1"
            else: # Fallback 1/2
                grid_cls += " md:grid-cols-2"
                col_txt, col_img = "", ""

        grid = html.DIV(Class=grid_cls)
        
        # --- Bloc Texte ---
        # max-w-prose pour une lecture agréable (65ch)
        txt_wrapper_cls = f"max-w-prose {col_txt if ratio != 'vertical' else ''}"
        if ratio != "vertical": txt_wrapper_cls += " md:max-w-none" # En grid, on laisse la grid gérer la largeur
        
        # Ordre (pour reverse)
        if reverse and ratio != "vertical":
            # Sur mobile (grid-cols-1), l'ordre HTML compte. Sur desktop, on pourrait utiliser order-last.
            # Ici, on va simplement inverser l'insertion dans le DOM plus bas.
            pass

        txt_div = html.DIV(Class=txt_wrapper_cls)
        txt_div <= html.H2(title, Class=f"text-2xl font-semibold {t['text_main']} sm:text-3xl")
        txt_div <= html.P(text, Class=f"mt-4 text-pretty {t['text_muted']}")
        
        # --- Bloc Image ---
        img_wrapper_cls = col_img if ratio != "vertical" else ""
        img_div = html.DIV(Class=img_wrapper_cls)
        
        if image:
            if isinstance(image, str):
                img_div <= html.IMG(src=image, alt=title, Class="rounded shadow-sm w-full object-cover")
            else:
                image.classList.add("rounded", "shadow-sm", "w-full", "object-cover")
                img_div <= image
        
        # --- Assemblage ---
        if ratio == "vertical":
            grid <= txt_div
            grid <= img_div
        else:
            if reverse:
                grid <= img_div
                grid <= txt_div
            else:
                grid <= txt_div
                grid <= img_div
                
        wrapper <= grid
        container <= wrapper
        return container


    # ==========================================
    # 53. COMPOSANTS DE STRUCTURE (TEAM)
    # ==========================================

    @staticmethod
    def Team(members, title=None, description=None, variant="base", extra_class=""):
        """
        Section de présentation d'équipe.
        
        Args:
            members: Liste de dicts:
                     {'name': 'Eric', 'role': 'Dev', 'image': 'url', 'bio': '...', 'social': '#'}
            title: Titre de la section.
            description: Intro de la section.
            variant: "base" (cartes rect), "bio" (avec description), "small" (avatars ronds).
        """
        t = UI.THEME
        
        section = html.SECTION(Class=f"{extra_class}")
        container = html.DIV(Class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8")
        
        # En-tête
        if title or description:
            header = html.DIV(Class="max-w-xl mb-12 text-center mx-auto")
            if title:
                header <= html.H2(title, Class=f"text-2xl font-bold {t['text_main']} sm:text-3xl")
            if description:
                header <= html.P(description, Class=f"mt-4 {t['text_muted']}")
            container <= header
            
        # Configuration Grille
        if variant == "small":
            grid_cls = "grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-6"
        else:
            grid_cls = "grid grid-cols-1 gap-8 md:grid-cols-3"
            
        grid = html.DIV(Class=grid_cls)
        
        for m in members:
            name = m.get("name", "Member")
            role = m.get("role", "")
            img_src = m.get("image", "")
            bio = m.get("bio", "")
            social_link = m.get("social")
            
            card = html.DIV()
            
            if variant == "small":
                # Style Avatar Rond
                if img_src:
                    card <= html.IMG(src=img_src, alt=name, Class="aspect-square w-full rounded-full object-cover mb-4")
                
                txt = html.DIV(Class="text-center")
                txt <= html.H3(name, Class=f"text-lg font-semibold {t['text_main']}")
                txt <= html.P(role, Class=f"text-sm {t['text_muted']}")
                card <= txt
                
            else:
                # Style Base Rectangulaire
                if img_src:
                    card <= html.IMG(src=img_src, alt=name, Class="aspect-video w-full rounded-lg object-cover mb-4")
                
                # Ligne Info + Social
                info_row = html.DIV(Class="flex items-center justify-between gap-4")
                
                # Info Gauche
                info_div = html.DIV()
                info_div <= html.H3(name, Class=f"text-lg font-semibold {t['text_main']}")
                info_div <= html.P(role, Class=f"text-sm {t['text_muted']}")
                info_row <= info_div
                
                # Social Droite
                if social_link:
                    sl = html.A(href=social_link, target="_blank", Class=f"text-{t['accent']}-600 transition hover:opacity-75")
                    # Icône générique (Link ou LinkedIn-like)
                    # On utilise un SVG simple pour l'exemple
                    svg = html.SVG(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 20 20", fill="currentColor", Class="size-6")
                    svg <= html.PATH(d="M16.338 16.338H13.67V12.16c0-.995-.017-2.277-1.387-2.277-1.39 0-1.601 1.086-1.601 2.207v4.248H8.014v-8.59h2.559v1.174h.037c.356-.675 1.227-1.387 2.526-1.387 2.703 0 3.203 1.778 3.203 4.092v4.711zM5.005 6.575a1.548 1.548 0 11-.003-3.096 1.548 1.548 0 01.003 3.096zm-1.337 9.763H6.34v-8.59H3.667v8.59zM17.668 1H2.328C1.595 1 1 1.581 1 2.298v15.403C1 18.418 1.595 19 2.328 19h15.34c.734 0 1.332-.582 1.332-1.299V2.298C19 1.581 18.402 1 17.668 1z")
                    sl <= svg
                    info_row <= sl
                    
                card <= info_row
                
                # Bio (si variant bio)
                if variant == "bio" and bio:
                    card <= html.P(bio, Class=f"mt-4 text-sm {t['text_muted']} leading-relaxed")

            grid <= card
            
        container <= grid
        section <= container
        return section    

