<?xml version="1.0" encoding="UTF-8" ?>
<Package name="rock-paper-scissors" format_version="5">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="NR_RPS_Demo" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="rps_rock" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="rps_scissors" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="rps_paper" xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs />
    <Resources>
        <File name="icon" src="icon.png" />
    </Resources>
    <Topics />
    <IgnoredPaths />
    <Translations auto-fill="en_US">
        <Translation name="translation_en_US" src="translations/translation_en_US.ts" language="en_US" />
        <Translation name="translation_nn_NO" src="translations/translation_nn_NO.ts" language="nn_NO" />
    </Translations>
</Package>
