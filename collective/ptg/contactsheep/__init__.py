from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import \
    BatchingDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.ptg.contactsheep')

class IContactsheepDisplaySettings(IBaseSettings):
    contactsheep_columns = schema.Int(
        title=_(u"label_contactsheep_columns",
            default=u"Number of images before a forced new row (use a high "
                    u"number if you dont want this)"),
        default=3,
        min=1)
    contactsheep_imagewidth = schema.Int(
        title=_(u"label_contactsheep_imagewidth",
            default=u"Width of (each) image (when mouse hovers)"),
        default=400,
        min=50)
    contactsheep_imageheight = schema.Int(
        title=_(u"label_contactsheep_imageheight",
            default=u"Height of (each) image"),
        default=260,
        min=50)
    contactsheep_use_icons = schema.Bool(
        title=_(u"label_contactsheep_use_icons",
            default=u"Use Thumbnail size instead of Size"),
        default=False)
    contactsheep_zoom = schema.Int(
        title=_(u"label_contactsheep_zoom",
            default=u"How many pixels to zoom when mouse over"),
        default=-10)
    contactsheep_overlay_opacity = schema.Choice(
        title=_(u"label_contactsheep_overlay_opacity",
                default=u"Opacity on mouse over"),
        default=0.3,
        vocabulary=SimpleVocabulary([
            SimpleTerm(0, 0,
                _(u"label_contactsheep_overlay_opacity0",
                    default=u"0 Off")),
            SimpleTerm(0.1, 0.1,
                _(u"label_contactsheep_overlay_opacity1",
                    default=u"0.1 Light")),
            SimpleTerm(0.2, 0.2,
                _(u"label_contactsheep_overlay_opacity2", default=u"0.2")),
            SimpleTerm(0.3, 0.3,
                _(u"label_contactsheep_overlay_opacity3", default=u"0.3")),
            SimpleTerm(0.4, 0.4,
                _(u"label_contactsheep_overlay_opacity4",
                    default=u"0.4 Medium")),
            SimpleTerm(0.5, 0.5,
                _(u"label_contactsheep_overlay_opacity5", default=u"0.5")),
            SimpleTerm(0.6, 0.6,
                _(u"label_contactsheep_overlay_opacity6",
                    default=u"0.6")),
            SimpleTerm(0.7, 0.7,
                _(u"label_contactsheep_overlay_opacity7",
                    default=u"0.7 Dark")),
            SimpleTerm(0.8, 0.8,
                _(u"label_contactsheep_overlay_opacity8",
                    default=u"0.8 Very Dark")),
            SimpleTerm(0.9, 0.9,
                _(u"label_contactsheep_overlay_opacity9",
                    default=u"0.9 Almost Black")),
            SimpleTerm(1, 1,
                _(u"label_contactsheep_overlay_opacity10",
                    default=u"1 Pitch Dark")
            )
        ]))

    contactsheep_style = schema.Choice(
        title=_(u"label_contactsheep_style",
                default=u"What stylesheet (css file) to use"),
        default="style.css",
        vocabulary=SimpleVocabulary([
            SimpleTerm("style.css", "style.css",
                _(u"label_contactsheep_style_default",
                    default=u"Default")),
            SimpleTerm("icon_style.css", "icon_style.css",
                _(u"label_contactsheep_style_icon",
                    default=u"Icon style (for small images)")),
            SimpleTerm("icon_style_ii.css", "icon_style_ii.css",
                _(u"label_contactsheep_style_icon_ii",
                    default=u"Icon style no 2")),
            SimpleTerm("icon_style_iii.css", "icon_style_iii.css",
                _(u"label_contactsheep_style_icon_iii",
                    default=u"Icon style no 3")),
            SimpleTerm("no_style.css", "no_style.css",
                _(u"label_contactsheep_style_no",
                    default=u"No style / css file")),
            SimpleTerm("custom_style", "custom_style",
                _(u"label_contactsheep_style_custom",
                    default=u"Custom css file")
            )
        ]))

    contactsheep_custom_style = schema.TextLine(
        title=_(u"label_custom_style",
            default=u"Name of Custom css file if you chose that above"),
        default=u"mycustomstyle.css")


class ContactsheepDisplayType(BatchingDisplayType):
    name = u"contactsheep"
    schema = IContactsheepDisplaySettings
    description = _(u"label_contactsheep_display_type",
        default=u"Contactsheep")

    def javascript(self):
        return u"""
     <script type="text/javascript">
$(document).ready(function() {
    $('.contactsheep a').mouseenter(function(e) {
        $(this).children('img').animate({
            height: '%(boxheight)i',
            left: '0',
            top: '0',
            width: '%(boxwidth)i'}, %(speed)i);
        $(this).children('div').fadeIn(%(speed)i);
    }).mouseleave(function(e) {
        $(this).children('img').animate({
            left: '%(zoom)i',
            top: '%(zoom)i',
            height: '%(imageheight)i',
            width: '%(imagewidth)i'}, %(speed)i);
        $(this).children('div').fadeOut(%(speed)i);
    });
});
</script>

""" % {
         'boxheight': self.settings.contactsheep_imageheight,
         'boxwidth': self.settings.contactsheep_imagewidth,
         'imageheight': self.settings.contactsheep_imageheight - (
            self.settings.contactsheep_zoom) * 2,
         'imagewidth': self.settings.contactsheep_imagewidth - (
            self.settings.contactsheep_zoom) * 2,
         'speed': self.settings.duration,
         'zoom': self.settings.contactsheep_zoom
    }

    def css(self):
        relpath = '++resource++ptg.contactsheep'
        style = '%s/%s/%s' % (self.portal_url, relpath,
            self.settings.contactsheep_style)

        if self.settings.contactsheep_style == 'custom_style':
            style = '%s/%s' % (self.portal_url,
                self.settings.contactsheep_custom_style)

        return u"""
        <style>
.contactsheep a img {
    height: %(imageheight)ipx;
    width: %(imagewidth)ipx;
    left: %(zoom)ipx;
    top: %(zoom)ipx;
}
.contactsheep a div,
.contactsheep a {
    height: %(boxheight)ipx;
    width: %(boxwidth)ipx;
}
.contactsheep a div {
    background-color: rgba(15, 15, 15, %(overlay_opacity)f);
}

</style>
<link rel="stylesheet" type="text/css" href="%(style)s"/>
""" % {
        'columns': self.settings.contactsheep_columns,
        'boxheight': self.settings.contactsheep_imageheight,
        'boxwidth': self.settings.contactsheep_imagewidth,
        'imageheight': self.settings.contactsheep_imageheight - (
            self.settings.contactsheep_zoom) * 2,
        'imagewidth': self.settings.contactsheep_imagewidth - (
            self.settings.contactsheep_zoom) * 2,
        'overlay_opacity': self.settings.contactsheep_overlay_opacity,
        'zoom': self.settings.contactsheep_zoom,
        'style': style
       }
ContactsheepSettings = createSettingsFactory(ContactsheepDisplayType.schema)
