# Licenses

Licenses seem like a "minor" thing but in a professional environment,
licenses are important in several ways.

## Choosing a license

Every code needs a license.
If you don't specify a license, no use from other professionals
is possible as your code bears a high legal risk.
Here is a rule of thumb:

- All projects using the code should be public: [GNU GPLv3][gplv3]
- Proprietary code: All Rights Reserved
- Free but 
- Free but mention me: [MIT License][mit-license]
- Don't care and want to communicate that: [WTFPL]

There are many more licenses and others might suit you better.
Some organizations even create own licenses to fit their own
needs.
If you want to check out the variety and details of licenses,
you can find and [overview here][licenses].
As we are not lawyers, we won't go into detail here and if you
have a use-case where detail matters, please consult a lawyer.

[gplv3]: https://www.gnu.org/licenses/gpl-3.0.en.html
[wtfpl]: https://en.wikipedia.org/wiki/WTFPL
[licenses]: https://choosealicense.com/licenses/
[mit-license]: https://choosealicense.com/licenses/mit/
[licenses]: https://en.wikipedia.org/wiki/Comparison_of_free_and_open-source_software_licenses

## Software Bill of Materials (SBOM)

If you ship a software, you also need to have a license and make sure
your license works with all the other software licenses from 
libraries.
A common way to realize this is to use a Software Bill of Materials.
As a software engineer, this clearing step can and should be
automated if you ship the software regularly.
Note that I also witnessed some bigger companies to do this manually.
Be aware, don't do this extra work of SBOM if you don't need it.

Advantages of SBOM are also:

- Understand Dependencies
- Detect Vulnerabilities
- Compliance Check

A tool to automate the SBOM creation is [cyclonedx].
Let's install it as a dev dependency:

```bash
poetry add --dev cyclonedx-bom
```

Now let's create the SBOM as a json file:

```bash
poetry run cyclonedx-bom \
    --poetry \
    --format json \
    --output sbom.json
```

Nice, now we have our SBOM as a file, but let's be honest no one
will ever read an unformatted json file nor check it.
To transform the output into a human readable markdown we can use
another package called `mdbom`.

```bash
poetry add --dev mdbom
```

`mdbom` requires a template file for the sbom but fortunately there is an
example.
Let's use it and store it under `docs/templates/sbom.md.jinja`:

```markdown
### 3rd Party Licenses

| Name                          | Version            | License(s)            | Type                   | URL                |
| ----------------------------- | ------------------ | --------------------- | ---------------------- | ------------------ |
| {% for package in packages %} | {{ package.name }} | {{ package.version }} | {{ package.licenses }} | {{ package.kind }} | {{ package.url }} |
{% endfor %}
```

Now let's run `mdbom`:

```bash
poetry run mdb generate \
    --input sbom.json \
    --output docs/sbom.md \
    --template docs/templates/sbom.md.jinja
```

And tada, we have our SBOM as a markdown file.
Later on we will include this in our docs so if a supervisor or customer bugs
us we can pinpoint them to the docs.
Since we are lazy don't forget to add the respective commands to the
`Taskfile.yaml`:

```yaml
  sbom:
    desc: Generate the Software Bill of Materials
    cmds:
      - |
        # Make sure no file exists since cyclonedx-bom cannot overwrite
        rm -f sbom.json
        # Create the Software Bill of Materials as json
        poetry run cyclonedx-bom \
          --poetry \
          --format json \
          --output sbom.json
        # Create the Software Bill of Materials as markdown
        poetry run mdb generate \
          --input sbom.json \
          --output docs/sbom.md \
          --template docs/templates/sbom.md.jinja
        # Clean up
        rm -f sbom.json

```

Lastly let's add `sbom.json` and `sbom.md`to the gitignore, since
we don't want to commit them with the source code itself.

```gitignore
# ...

# ignore sbom files
sbom.json
sbom.md
```

[cyclonedx]: https://github.com/CycloneDX/cyclonedx-python
