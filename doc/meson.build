expand_content_md_files = [
  'internals.md',
  'plugin-examples.md',
  'plugin-guide.md'
]

website_pages = [
  'index.html',
  'plugins.html'
]

website_deps = [
  'pages.py',
  'page.html',
  meson.project_source_root() / 'NEWS'
]

toml_data = configuration_data()
toml_data.set('VERSION', meson.project_version())

rb_toml = configure_file(
  input: 'rhythmbox.toml.in',
  output: 'rhythmbox.toml',
  configuration: toml_data
)

gidocgen = find_program('gi-docgen')

fs = import('fs')
fs.copyfile(meson.project_source_root() / 'data/icons/hicolor/scalable/apps/org.gnome.Rhythmbox3.svg')

custom_target('apidoc',
  input: [ rb_toml, rb_gir ],
  output: 'apidoc',
  command: [
    gidocgen,
    'generate',
    '--quiet',
    '--add-include-path=@0@'.format(meson.current_build_dir() / '../lib/libmediaplayerid'),
    '--config=@INPUT0@',
    '--output-dir=@OUTPUT@',
    '--no-namespace-dir',
    '--content-dir=@0@'.format(meson.current_source_dir()),
    '@INPUT1@',
  ],
  depend_files: [ expand_content_md_files ],
  build_by_default: true,
)

custom_target('website',
  input: website_pages,
  output: website_pages,
  depend_files: website_deps,
  command: [
    find_program('pages.py'),
    '@SOURCE_ROOT@:@SOURCE_ROOT@/doc',
    '@OUTPUT@'
  ],
  build_by_default: true,
)
