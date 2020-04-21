# specify the dependency versions (can be overriden with --build_arg)
ARG quilc_version=1.16.1
ARG qvm_version=1.15.3

# use multi-stage builds to independently pull dependency versions
FROM rigetti/quilc:$quilc_version as quilc
FROM rigetti/qvm:$qvm_version as qvm
FROM jupyter/minimal-notebook:latest

# copy over the pre-built quilc binary from the first build stage
COPY --from=quilc /src/quilc/quilc /src/quilc/quilc

# copy over the pre-built qvm binary from the second build stage
COPY --from=qvm /src/qvm/qvm /src/qvm/qvm

USER root
# install the missing apt packages that aren't copied over
RUN apt-get update && apt-get -yq dist-upgrade && \
    apt-get install --no-install-recommends -yq \
    git libblas-dev libffi-dev liblapack-dev libzmq3-dev \
    texlive-latex-base texlive-fonts-recommended texlive-fonts-extra \
    texlive-latex-extra libjbig0 imagemagick ghostscript && \
    sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read|write" pattern="PDF" \/>/g' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policy domain="path" rights="none"/<policy domain="path" rights="read|write"/g' /etc/ImageMagick-6/policy.xml && \
    rm -rf /var/lib/apt/lists/*

ADD . /src/pyquil

RUN chown -R jovyan.users /src

# Switch back to jovyan to avoid accidental container runs as root
USER jovyan

# copy over files 

WORKDIR /src/pyquil
RUN mkdir  -p ~/texmf/tex/generic/pgf/quantikz && \
    mv tikzlibraryquantikz.code.tex ~/texmf/tex/generic/pgf/quantikz/ 
    
# install pyquil
RUN python -m pip install pyquil && \
    python -m pip install pdflatex && \
    python -m pip install convert

# use an entrypoint script to add startup commands (qvm & quilc server spinup)
ENTRYPOINT ["tini", "-g", "--"]
CMD ["/src/pyquil/entrypoint.sh"]

