#!/usr/bin/python
# -*- coding: utf-8 -*-

# MySQL Dump System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# Improved for SilverStripe SSPAK dumps by Simon `Firesphere` Erkelens
#
# This file is part of MySQL Dump System.
#
# MySQL Dump System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MySQL Dump System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MySQL Dump System. If not, see <http://www.gnu.org/licenses/>.

# This code has been amended with support for gzip, single-file dumps and improved
# code. All licensed under GPL-3. Additional changes made by Simon `Firesphere` Erkelens
# Changes are marked in the changelog or on GitHub, publicly hosted.

__author__ = "João Magalhães <joamag@hive.pt>, Simon `Firesphere` Erkelens <github@casa-laguna.net>"
""" The author(s) of the module """

__version__ = "3.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda. & Firesphere Code Companions"
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import datetime
import getopt
import gzip
import os
import shutil
import sys
import time
import zipfile

import legacy
import pymysql

VERSION = "0.3.0"
""" The current version value for the mysql dump executable """

RELEASE = "150"
""" The release value, should be an internal value related
with the build process """

BUILD = "3"
""" The build value, representing the sub release value
existent in the build process """

RELEASE_DATE = "2019"
""" The release date value for the current version """

BRANDING_TEXT = "MySQL Dump System %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value the template based values
should be defined as constants """

SSPAK_TEXT = "Python SSPAK by Simon `Firesphere` Erkelens, improved version for SilverStripe. " \
             "Original by:" + BRANDING_TEXT
""" SSPAK release"""

VERSION_PRE_TEXT = "Python 3.x"
""" The version pre text value, that appears before the printing
of the branding text second line """

CONVERSION = {
    str: lambda v: "'%s'" % _escape(v),
    legacy.UNICODE: lambda v: "'%s'" % _escape(v.encode("utf-8")),
    int: lambda v: str(v),
    legacy.LONG: lambda v: str(v),
    float: lambda v: str(v),
    datetime.datetime: lambda v: "'%s'" % v,
    type(None): lambda v: "null",
}
""" Conversion map to be used to convert python types
into mysql string value types """

RESOLVE = {
    "PRI": "primary key"
}
""" Resolution map used to resolve the some of the table information
into the equivalent schema oriented values """

QUIET = False
""" The global "static" flag that control if any output should
be sent to the standard output / error """


class Exporter(object):

    def __init__(self, database, host=None, user=None, password=None, file_path=None, compression='gz'):
        self.database = database
        self.host = host or "127.0.0.1"
        self.user = user or "root"
        self.password = password or ""
        self.file_path = file_path or "export.sql.%s" % compression
        self.temp_path = "export"
        self.connection = None
        self.compression = compression

    def connect(self):
        if self.connection: return
        self.connection = pymysql.connect(
            self.host,
            user=self.user,
            passwd=self.password,
            db=self.database
        )

    def ensure(self):
        if self.connection:
            return
        self.connect()

    def dump(self):
        print_message("------------------------------------------------------------------------")
        print_message("Dumping '%s@%s' database into '%s'" % (self.database, self.host, self.temp_path))
        initial = time.time()

        self.connect()
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)

        try:
            self.dump_schema()
            self.dump_tables()
            self.compress(self.file_path, self.compression)
        finally:
            shutil.rmtree(self.temp_path, ignore_errors=True)

        final = time.time()
        delta = final - initial
        print_message("Finished dumping of database in %d seconds" % delta)

    def dump_schema(self):
        file_path = os.path.join(self.temp_path, "database.sql")
        file = open(file_path, "ab")
        self._write_file(file, "/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n\
/*!40101 SET NAMES utf8 */;\n\
/*!50503 SET NAMES utf8mb4 */;\n\
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;\n\
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;\n\n")
        try:
            self._dump_schema(file)
        finally:
            file.close()

    def _write_file(self, file, data, encoding="utf-8"):
        if type(data) == legacy.UNICODE:
            data = data.encode(encoding)
        file.write(data)

    def _dump_schema(self, file):
        print_message("Dumping the table schema into schema file...")
        initial = time.time()

        tables = self.fetch_single(
            "SELECT `table_name` FROM `information_schema`.`tables` WHERE `table_schema` = '%s'" % self.database
        )

        # retrieves the current tables length (amount of tables)
        # so that it's possible to calculate the percentage of
        # completion for the current process
        tables_l = len(tables)
        index = 1

        for table in tables:
            reset_line()
            print_message("\r[%d/%d] - %s" % (index, tables_l, table), False)

            columns = self.fetch_all(
                "SELECT `column_name`, `column_type`, `column_key`, `column_default`, `extra`, `character_set_name`\
                     FROM `information_schema`.`columns`\
                     WHERE `table_schema` = '%s' AND `table_name` = '%s'" %
                (self.database, table)
            )
            collation = self.fetch_one(
                "SELECT `ENGINE`, `TABLE_COLLATION`\
                    FROM `information_schema`.`TABLES`\
                    WHERE `table_schema` = '%s' AND `table_name` = '%s'" %
                (self.database, table))
            charset = collation[1].split('_')
            keys = [column[0] for column in columns if column[2] == "PRI"]
            keys_mul = [column[0] for column in columns if column[2] == "MUL"]
            keys_s = ", ".join(keys)

            self._write_file(file, "CREATE TABLE IF NOT EXISTS `%s` (\n" % table)
            # @todo clean this up to be more readable
            for column in columns:
                column = list(column)
                default = column[3]
                if column[3] is None:
                    default = 'NULL'

                column_string = "`" + column[0] + "` " + column[1]
                if column[4] in ['auto_increment']:
                    column_string += ' NOT NULL AUTO_INCREMENT'
                elif column[5] is not None:
                    column_string += ' CHARACTER SET %s COLLATE %s' % (charset[0], collation[1])
                if column[3] is not None and column[4] != 'auto_increment':
                    column_string += " DEFAULT '" + default.replace('\\', '\\\\') + "'"
                self._write_file(
                    file,
                    "    %s,\n" % column_string
                )

            self._write_file(file, "    PRIMARY KEY(%s)" % keys_s)
            for mulkey in keys_mul:
                self._write_file(
                    file,
                    ",\n    KEY `%s` (`%s`)" % (mulkey, mulkey)
                )
            self._write_file(file, "\n)")
            if collation[0] is not None:
                self._write_file(
                    file,
                    " ENGINE=%s DEFAULT CHARSET=%s COLLATE=%s" %
                    (collation[0], charset[0], collation[1])
                )
            self._write_file(file, ";\n\n")
            self._write_file(file, "/*!40000 ALTER TABLE `%s` DISABLE KEYS */;\n" % table)
            self._write_file(file, "/*!40000 ALTER TABLE `%s` ENABLE KEYS */;\n\n" % table)

            index += 1

        final = time.time()
        delta = final - initial
        reset_line()
        print_message("\rDumped table schema in %d seconds" % delta)

    def dump_tables(self):
        print_message("Dumping the table data into data files...")
        initial = time.time()

        tables = self.fetch_single(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = '%s'" % self.database
        )

        # retrieves the current tables length (amount of tables)
        # so that it's possible to calculate the percentage of
        # completion for the current process
        tables_l = len(tables)
        index = 1
        file_path = os.path.join(self.temp_path, "database.sql")
        file = open(file_path, "ab")

        for table in tables:
            reset_line()
            print_message("\r[%d/%d] - %s" % (index, tables_l, table), False)

            columns = self.fetch_single(
                "SELECT `column_name` FROM `information_schema`.`columns` "
                "WHERE `table_schema` = '%s' AND `table_name` = '%s'" %
                (self.database, table)
            )
            columns_s = "`, `".join(columns)
            data = self.fetch_all(
                "SELECT `%s` FROM `%s`" % (columns_s, table)
            )

            self._write_file(file, "DELETE FROM `%s`;\n" % table)
            if len(data):
                self._write_file(file, "/*!40000 ALTER TABLE `%s` DISABLE KEYS */;\n" % table)
                self._write_file(file, "/*!40000 ALTER TABLE `%s` ENABLE KEYS */;\n\n" % table)
                # Split in to chunks of 100 items per chunk to not crash the database
                chunks = [data[x:x + 1024] for x in range(0, len(data), 1024)]
                for chunk in chunks:
                    self._write_file(file, "INSERT INTO `%s` (`%s`) VALUES " % (table, columns_s))
                    self.dump_data(file, chunk)
            index += 1

        # Reset the SQL Modes to what it's supposed to be :)
        self._write_file(file, "/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;\n")
        self._write_file(
            file,
            "/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;\n"
        )
        self._write_file(file, "/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;")

        file.close()
        final = time.time()
        delta = final - initial
        reset_line()
        print_message("\r\nDumped table data in %d seconds" % delta)

    def dump_data(self, file, data):
        for item in data:
            self._write_file(file, "(")
            is_first = True
            for value in item:
                if is_first:
                    is_first = False
                else:
                    self._write_file(file, ",")
                value_t = type(value)
                value_f = CONVERSION.get(value_t, str)
                value_s = value_f(value)
                self._write_file(file, value_s)
            self._write_file(file, "),\n")
        # Trim off the final comma and close the command. SEEK_END is most efficient
        file.seek(-2, os.SEEK_END)
        file.truncate()
        self._write_file(file, ";\n\n")

    def compress(self, target=None, compression='gz'):
        target = target or self.file_path
        print_message("Compressing database information into database.sql.%s..." % compression)
        initial = time.time()

        # Make sure the compression extension is in the file name
        if "." + compression not in target:
            target = target + "." + compression

        for base, _dirs, files in os.walk(self.temp_path):
            for file in files:
                # gzip compression support
                if compression == 'gz':
                    with open(os.path.join(base, file), 'rb') as inputdata:
                        with gzip.open(target, 'w') as output:
                            shutil.copyfileobj(inputdata, output)
                if compression == 'zip':
                    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zipArchive:
                        root_l = len(self.temp_path) + 1
                        path = os.path.join(base, file)
                        zipArchive.write(path, path[root_l:])

        final = time.time()
        delta = final - initial
        print_message("Compressed database information in %d seconds" % delta)

    def fetch_one(self, query):
        self.ensure()
        cursor = self.connection.cursor()
        cursor.execute(query)
        try:
            data = cursor.fetchone()
        finally:
            cursor.close()
        return data

    def fetch_all(self, query):
        self.ensure()
        cursor = self.connection.cursor()
        cursor.execute(query)
        try:
            data = cursor.fetchall()
        finally:
            cursor.close()
        return data

    def fetch_single(self, query):
        data = self.fetch_all(query)
        elements = [item[0] for item in data]
        return elements


def reset_line():
    line = "\r" + (" " * 78)
    print_message(line, False)


def print_message(message, newline=True):
    # @todo make this a generic service instead of MySQL Dump
    if QUIET:
        return
    sys.stdout.write(message)
    newline and sys.stdout.write("\n")


def dump(database, host=None, user=None, password=None, file_path=None, compression='gz'):
    exporter = Exporter(
        database,
        host=host,
        user=user,
        password=password,
        file_path=file_path,
        compression=compression
    )
    exporter.dump()


def information():
    # print the branding information text and then displays
    # the python specific information in the screen
    print_message(BRANDING_TEXT % (VERSION, RELEASE, BUILD, RELEASE_DATE))
    print_message(VERSION_PRE_TEXT + sys.version)


def help():
    print_message("Usage:")
    print_message("mysql_dump [--quiet] [--help] [--host=] [--user=] [--password=]\n\
    [--database=] [--file=], [--compression=]")


def _escape(value):
    return pymysql.escape_string(value.decode())


def main():
    global QUIET

    database = "default"
    host = "127.0.0.1"
    user = ""
    password = ""

    # parses the various options from the command line and then
    # iterates over the map of them top set the appropriate values
    # for the variables associated with the options
    _options, _arguments = getopt.getopt(sys.argv[1:], "hqd:h:u:p:f:c:", [
        "help",
        "quiet",
        "database=",
        "host=",
        "user=",
        "password=",
        "file=",
        "compression="
    ])
    for option, argument in _options:
        if option in ("-h", "--help"):
            help()
            exit(0)
        elif option in ("-q", "--quiet"):
            QUIET = True
        elif option in ("-d", "--database"):
            database = argument
        elif option in ("-h", "--host"):
            host = argument
        elif option in ("-u", "--user"):
            user = argument
        elif option in ("-p", "--password"):
            password = argument

    information()
    dump(
        database,
        host=host,
        user=user,
        password=password,
        compression='gz'
    )


if __name__ == "__main__":
    main()
