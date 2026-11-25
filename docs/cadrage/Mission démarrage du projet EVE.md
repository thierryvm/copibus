# **EVE – Cahier des charges et étude approfondie, version de cadrage 1.0**

Tes précisions changent sensiblement l'ambition du projet. Je vais donc intégrer ces éléments comme des exigences du produit, et pas comme de simples options.

Il y a notamment cinq décisions importantes que je prends pour la conception :

1. **EVE sera indépendante de Keolis et du TEC au départ.** Elle fonctionnera avec les données publiques et les informations introduites par les chauffeurs. Une intégration officielle sera possible ultérieurement.
2. **Le produit sera pensé pour plusieurs entreprises de transport**, et pas seulement pour Keolis. Un chauffeur pourra sélectionner son entreprise, son dépôt, ses lignes et ses véhicules.
3. **Le fonctionnement de base sera gratuit**, sans abonnement obligatoire à une IA. Les abonnements personnels Claude, ChatGPT ou Gemini seront des intégrations facultatives.
4. **La première version sera accessible par un simple lien web installable sur le téléphone**, sans compte développeur Apple. Une application native pourra venir ensuite.
5. **La sécurité des itinéraires et des véhicules sera une priorité absolue.** EVE pourra signaler un danger et proposer une alternative, mais ne présentera jamais une déviation comme sûre sans validation des contraintes réelles du véhicule et de la réglementation.

Une précision technique : le matériel que tu appelles APF est bien la PFE (plateforme embarquée), d'après la terminologie que l'on retrouve dans les informations relatives au suivi des bus TEC.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://letecfinder.be\&sz=32)

Letec Finder



Autre point essentiel pour le tachygraphe : les services réguliers de transport de voyageurs dont le parcours ne dépasse pas 50 km bénéficient d'une exemption au règlement européen 561/2006. Cela ne signifie pas que tous les services de bus sont exemptés, ni que toutes les obligations sociales et professionnelles disparaissent. Les services spéciaux, occasionnels, internationaux et les navettes doivent être classifiés correctement avant de calculer les obligations applicables.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://eur-lex.europa.eu\&sz=32)

EUR-Lex+2



## **20. Résultats importants de l'étude complémentaire**

Voici quelques conclusions qui méritent d'être soulignées avant de passer au développement.

### **Le réseau TEC et les entreprises sous-traitantes**

L'OTW regroupe les activités TEC depuis 2019. Ses différentes unités territoriales comprennent notamment Liège-Verviers et Namur-Luxembourg.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.wallonie.be\&sz=32)

wallonie.be



J'ai également retrouvé un répertoire particulièrement utile : celui de la FBAA, qui recense les entreprises belges d'autobus et d'autocars.

Pour la province de Liège, on retrouve notamment :

- Compagnie des Autobus Liégeois – Sprimont.
- Autocars Jacky – Aywaille.
- Autobus F. Gohy – Theux.
- Eurobussing Wallonie – Flémalle.
- Garage du Perron – Verviers.
- SADAR – Kelmis.
- Satracom – Waimes.
- Transcar – Seraing.
- Voyages Léonard – Blegny.

Pour Namur, le répertoire comprend notamment Roquet, Deblire Autocars et Latour Autobus.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.fbaa.be\&sz=32)

FBAA



Ce sera notre point de départ pour constituer le catalogue national des entreprises et dépôts. Il faudra cependant vérifier séparément les marchés TEC réellement attribués à chaque entreprise.

[Répertoire officiel des entreprises membres de la FBAA](https://www.fbaa.be/fr/entrepreneurs/localisateur-dentreprises?utm_source=chatgpt.com)

### **La navigation et les positions des bus**

J'ai identifié un élément intéressant : le portail belge documente bien un flux de positions des véhicules TEC, en complément des horaires estimés et des perturbations. Les flux SIRI sont actualisés environ toutes les 30 secondes.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://data.belgianmobility.io\&sz=32)

Belgian Mobility Open Data Portal+1



Il faudra donc développer deux systèmes complémentaires :

- Le GPS de ton téléphone, pour suivre ta progression sur la route avec une carte fluide.
- Les positions des véhicules TEC, pour visualiser les autres bus lorsque leurs positions sont disponibles.

Attention : les 30 secondes concernent l'actualisation annoncée du flux public, pas la fréquence du GPS de ton téléphone.

### **La déviation adaptée au véhicule**

J'ai confirmé que Valhalla possède un profil de routage autobus avec des paramètres de hauteur, largeur, longueur et poids.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://valhalla.github.io\&sz=32)

Valhalla Docs



C'est une bonne base technique, mais pas une garantie de sécurité. EVE devra aussi connaître les restrictions temporaires, les limitations de tonnage, les accès interdits et les caractéristiques de giration.

Je propose donc une règle non négociable : une déviation calculée par EVE sera présentée comme une proposition à vérifier, jamais comme un itinéraire garanti sûr.

### **Le modèle économique et les services gratuits**

Il y a une distinction essentielle à faire :

| Service             | Gratuit              | Payant                               |
| ------------------- | -------------------- | ------------------------------------ |
| Données TEC de base | Oui                  | Historique et quotas supérieurs      |
| Supabase            | Prototype            | Production évoluée                   |
| Vercel              | Projet personnel     | Usage professionnel évolutif         |
| OpenStreetMap       | Données              | Hébergement de tuiles éventuellement |
| Open-Meteo          | Usage non commercial | Licence commerciale                  |
| IA personnelle      | Sans coût EVE        | API payée par l'utilisateur          |
| IA hébergée par EVE | Quota éventuel       | Crédits premium                      |

Le point important est Open-Meteo : son offre gratuite est réservée à l'utilisation non commerciale. Si EVE devient un service payant, il faudra une licence commerciale ou une solution auto-hébergée.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://open-meteo.com\&sz=32)

Open-Meteo.com+1



Concernant ton infrastructure actuelle, Supabase Free et Vercel Hobby conviennent pour commencer à expérimenter, mais je ne les considérerais pas comme une infrastructure de production garantie. Vercel indique notamment que Hobby est réservé aux projets personnels et non commerciaux ; son offre Pro est affichée à 20 USD/mois. Supabase Pro commence à 25 USD/mois.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://vercel.com\&sz=32)

vercel.com+1



# **21. Le document PRD est prêt**

**EVE – PRD et étude technique v1.0**

Markdown · Environ 65 Ko · 23 novembre 2026

Prêt

Le document contient :

- Vision et exigences fonctionnelles.
- Architecture technique.
- Inventaire des API.
- Gestion des entreprises, dépôts, lignes et véhicules.
- Planning OCR et échanges de services.
- Navigation GPS et alertes.
- Check-lists et rapports d'avaries.
- Tachygraphe et réglementation.
- RGPD et sécurité.
- Modèle économique.
- Roadmap et critères d'acceptation.
- Instructions destinées à Claude Code.

  &#x20;Télécharger le PRD

## **22. Le nom : attention à ne pas se précipiter**

J'ai déjà écarté plusieurs pistes qui existent dans des activités proches : Navelys, Lignova et Conduvia notamment.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.navelys.com\&sz=32)

Leader Européen du Transport en Autocar+3



Je conserverais provisoirement cette piste :

**Buselium — EVE, votre copilote professionnelle.**

Mais je ne prétends pas que `buselium.be` est disponible. La recherche sur Internet ne suffit pas pour certifier la disponibilité d'un nom de domaine ou d'une marque. Il faut vérifier les registres DNS Belgium, BOIP et EUIPO avant de retenir définitivement le nom.

[Vérifier un domaine .be](https://www.dnsbelgium.be/en/?utm_source=chatgpt.com) · [Vérifier les marques Benelux](https://www.boip.int/?utm_source=chatgpt.com) · [Vérifier les marques européennes](https://euipo.europa.eu/?utm_source=chatgpt.com)

## **23. Le premier travail à confier à Claude Code**

Je te conseille de ne pas lui demander immédiatement de développer toute l'application.

Il faut d'abord qu'il examine ton environnement Vercel/Supabase, qu'il établisse l'architecture et qu'il valide les sources de données. Ensuite seulement, il pourra construire les premiers modules.

Voici le prompt de lancement que je te recommande :

# Mission : démarrage du projet EVE

Tu es l'architecte logiciel et le développeur principal du projet EVE, une copilote intelligente destinée aux conducteurs professionnels d'autobus et d'autocars en Belgique.

Tu trouveras en pièce jointe le document `EVE_PRD_Cadrage_v1.0.md`.

Ce document constitue la base fonctionnelle du projet, mais il ne doit pas être considéré comme une architecture technique définitivement figée.

## Première mission : audit et préparation

Avant de développer quoi que ce soit :

1. Examine intégralement le PRD.
2. Audite l'environnement technique existant, les comptes et projets Vercel et Supabase, ainsi que les éventuels dépôts Git.
3. Vérifie les API et services externes mentionnés dans le document.
4. Vérifie leurs licences, limitations, coûts et conditions d'utilisation.
5. Évalue les contraintes iOS, Android et PWA.
6. Propose une architecture simple, sécurisée, évolutive et adaptée à un développeur non professionnel utilisant Claude Code.

## Principes impératifs

- Ne jamais inventer une API ou une capacité technique.
- Ne pas engager de dépenses sans validation.
- Ne pas introduire de dépendance payante obligatoire pour les fonctions fondamentales.
- Privilégier les solutions open source et les données publiques.
- Prévoir une architecture multi-entreprises.
- Garantir l'isolation des données et la sécurité des comptes.
- Ne jamais présenter une déviation routière comme sûre sans validation.
- Respecter les exigences RGPD et les restrictions des systèmes mobiles.
- Prévoir des tests réels sur iPhone et Android.

## Livrables de cette première mission

1. Rapport d'audit technique.
2. Architecture cible argumentée.
3. Liste des risques et limitations.
4. Comparatif des technologies envisagées.
5. Vérification des API TEC et des flux temps réel.
6. Schéma de base de données initial.
7. Plan de sécurité et de gestion des accès.
8. Roadmap de développement découpée en étapes indépendantes.
9. Estimation des coûts mensuels à chaque étape.

Ne commence pas encore le développement complet.

Tu dois pouvoir remettre en question mes choix et ceux du PRD lorsque tu identifies une solution plus fiable, plus simple ou plus économique.

La priorité absolue est de construire une application professionnelle fiable, sécurisée et facile à utiliser, sans complexité inutile.

**Ma recommandation finale :** construisons d'abord une version pilote pour toi et quelques collègues, avec les vrais horaires, les vrais services, les vrais véhicules et les véritables parcours TEC.

C'est en l'utilisant quotidiennement que nous découvrirons les détails qui feront la différence entre une application sympathique et une véritable copilote professionnelle.

Et je garderais une idée en tête pour la suite : **EVE ne doit pas simplement connaître les horaires des bus. Elle doit connaître le travail du conducteur.**