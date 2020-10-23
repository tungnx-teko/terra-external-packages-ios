@file:Suppress("UNCHECKED_CAST")

import groovy.json.JsonSlurper
import groovy.util.Node
import org.gradle.api.publish.maven.MavenPom

plugins {
    kotlin("jvm") version "1.4.10"
    id("maven-publish")
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))
}

publishing {
    repositories {
        maven {
            name = "TerraExternalPackages"
            url = uri("https://maven.pkg.github.com/teko-vn/terra-external-packages")
            credentials {
                username = System.getenv("GITHUB_USER_NAME")
                password = System.getenv("GITHUB_USER_TOKEN")
            }
        }
    }
    publications.create<MavenPublication>("release") {
        afterEvaluate {
            File("build/outputs")
                .listFiles { pathname -> pathname.isFile && pathname.exists() && pathname.extension == "json" }
                .orEmpty()
                .forEach { properties ->
                    val json = JsonSlurper().parseText(properties.readText())
                    val artifactProperties = parseArtifactProperties(json as Map<String, Any>)
                    if (artifactProperties.isValid()) {
                        groupId = "vn.teko.android.packages"
                        artifactId = artifactProperties.id
                        version = artifactProperties.version
                        artifact("build/outputs/${artifactProperties.name}")

                        pom {
                            fillGenericDetails()
                            fillDependencies(artifactProperties.dependencies)
                        }
                    }
                }
        }
    }
}

fun MavenPom.fillGenericDetails() {
    name.set("Terra external packages")
    packaging = "aar"
    description.set("External packages for Terra platform")
    url.set("https://github.com/teko-vn/terra-external-packages")

    scm {
        url.set("https://github.com/teko-vn/terra-external-packages")
        connection.set("scm:git@github.com:teko-vn/terra-external-packages.git")
        developerConnection.set("scm:git@github.com:teko-vn/terra-external-packages.git")
    }

    developers {
        developer {
            id.set("teko-vn")
            name.set("Mobile Lab")
            email.set("mobile.lab@teko.vn")
            organization.set("Teko")
            organizationUrl.set("https://teko.vn/")
        }
    }
}

fun MavenPom.fillDependencies(dependencies: List<Dependency>) {
    withXml {
        if (dependencies.isNotEmpty()) asNode().appendDependencies(dependencies)
    }
}

fun Node.appendDependencies(
    dependencies: List<Dependency>
) = appendNode("dependencies").apply {
    dependencies.forEach { appendDependency(it) }
}

fun Node.appendDependency(
    dependency: Dependency
) = appendNode("dependency").apply {
    appendNode("groupId", dependency.groupId)
    appendNode("artifactId", dependency.artifactId)
    appendNode("version", dependency.version)
    appendNode("scope", dependency.scope)

    if (dependency.exclusions.isNotEmpty()) appendExclusions(dependency.exclusions)
}

fun Node.appendExclusions(
    exclusions: List<Exclusion>
) = appendNode("exclusions").apply {
    exclusions.forEach { appendExclusion(it) }
}

fun Node.appendExclusion(
    exclusion: Exclusion
) = appendNode("exclusion").apply {
    appendNode("groupId", exclusion.groupId)
    appendNode("artifactId", exclusion.artifactId)
}

fun parseArtifactProperties(json: Map<String, Any>): ArtifactProperties {
    val dependencies = mutableListOf<Dependency>()
    (json["dependencies"] as? List<Map<String, Any>>)?.forEach {
        val exclusions = mutableListOf<Exclusion>()
        (it["exclusions"] as? List<Map<String, Any>>)?.forEach {
            val exclusion = Exclusion(
                it.getAsString("groupId"),
                it.getAsString("artifactId")
            )
            if (exclusion.isValid()) exclusions.add(exclusion)
        }

        val dependency = Dependency(
            it.getAsString("scope"),
            it.getAsString("groupId"),
            it.getAsString("artifactId"),
            it.getAsString("version"),
            exclusions
        )
        if (dependency.isValid()) dependencies.add(dependency)
    }

    return ArtifactProperties(
        json.getAsString("id"),
        json.getAsString("name"),
        json.getAsString("version"),
        dependencies
    )
}

fun Map<String, Any>.getAsString(key: String, default: String = ""): String {
    return this[key] as? String ?: default
}

data class ArtifactProperties(
    val id: String,
    val name: String,
    val version: String,
    val dependencies: List<Dependency>
)

fun ArtifactProperties.isValid() = id.isNotBlank() && name.isNotBlank() && version.isNotBlank()

data class Dependency(
    val scope: String,
    val groupId: String,
    val artifactId: String,
    val version: String,
    val exclusions: List<Exclusion>
)

fun Dependency.isValid() = groupId.isNotBlank() && artifactId.isNotBlank() && version.isNotBlank() && scope.isNotBlank()

data class Exclusion(
    val groupId: String,
    val artifactId: String
)

fun Exclusion.isValid() = groupId.isNotBlank() && artifactId.isNotBlank()